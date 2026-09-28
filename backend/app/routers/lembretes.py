from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.db import db, now
from app.dependencies import get_current_user
from app.schemas.lembrete import (
    EnviarLembreteRequest,
    EnvioResultado,
    LembreteCreate,
    LembreteMensagemUpdate,
    LembreteResponse,
    LembreteVesperaResponse,
    WhatsAppConfigResponse,
)
from app.services import lembretes as svc
from app.services import whatsapp

router = APIRouter(prefix="/lembretes", tags=["lembretes"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[LembreteResponse])
async def listar():
    return await crud.listar(db.lembretes, LembreteResponse, ordem=-1)


@router.post("/", response_model=LembreteResponse, status_code=201)
async def criar(body: LembreteCreate):
    return await crud.criar(db.lembretes, LembreteResponse, body, {"criado_em": now(), "salao_id": 1})


# ---------- Lembretes de véspera ----------


@router.get("/config", response_model=WhatsAppConfigResponse)
async def config_whatsapp():
    return WhatsAppConfigResponse(
        twilio_configurado=whatsapp.configurado(),
        sandbox=whatsapp.usando_sandbox(),
        remetente=whatsapp.remetente_mascarado(),
    )


@router.get("/vespera", response_model=list[LembreteVesperaResponse])
async def listar_vespera():
    return await svc.listar_amanha()


@router.put("/vespera/{agendamento_id}", response_model=LembreteVesperaResponse)
async def editar_mensagem(agendamento_id: str, body: LembreteMensagemUpdate):
    return await svc.salvar_mensagem(agendamento_id, body.mensagem)


async def _enviar(item: LembreteVesperaResponse, canal: str, mensagem: str | None) -> EnvioResultado:
    texto = (mensagem or item.lembrete.mensagem or "").strip()
    if not texto:
        return EnvioResultado(agendamento_id=item.id, ok=False, detalhe="Gere ou escreva a mensagem antes de enviar", item=item)
    if texto != item.lembrete.mensagem:
        item = await svc.salvar_mensagem(item.id, texto)

    if canal == "twilio":
        if not item.telefone_e164:
            return EnvioResultado(agendamento_id=item.id, ok=False, detalhe="Telefone da cliente inválido", item=item)
        try:
            sid = await whatsapp.enviar(item.telefone_e164, texto)
        except whatsapp.EnvioWhatsAppError as exc:
            item = await svc.registrar_erro(item, str(exc))
            return EnvioResultado(agendamento_id=item.id, ok=False, detalhe=str(exc), item=item)
        item = await svc.registrar_envio(item, "twilio", texto, sid)
    else:
        item = await svc.registrar_envio(item, "whatsapp_link", texto)
    return EnvioResultado(agendamento_id=item.id, ok=True, item=item)


@router.post("/vespera/enviar-todos", response_model=list[EnvioResultado])
async def enviar_todos():
    if not whatsapp.configurado():
        raise HTTPException(status_code=503, detail="Envio automático desativado: configure TWILIO_* no backend/.env")
    pendentes = [i for i in await svc.listar_amanha() if i.lembrete.mensagem and not i.lembrete.enviado_em]
    return [await _enviar(i, "twilio", None) for i in pendentes]


@router.post("/vespera/{agendamento_id}/enviar", response_model=EnvioResultado)
async def enviar_um(agendamento_id: str, body: EnviarLembreteRequest):
    item = await svc.obter(agendamento_id)
    if body.canal == "twilio" and not whatsapp.configurado():
        raise HTTPException(status_code=503, detail="Envio automático desativado: configure TWILIO_* no backend/.env")
    return await _enviar(item, body.canal, body.mensagem)
