"""Lembretes de véspera: agendamentos de amanhã + geração/envio de mensagens."""

from bson import ObjectId
from fastapi import HTTPException
from pymongo import ReturnDocument

from app.db import db, janela_dia, now, oid
from app.schemas.lembrete import LembreteVesperaResponse
from app.services.whatsapp import normalizar_telefone

STATUS_ATIVOS = ("confirmado", "pendente")


async def _mapa(col, ids: list[ObjectId]) -> dict:
    return {d["_id"]: d for d in await col.find({"_id": {"$in": ids}}).to_list(len(ids) or 1)} if ids else {}


async def _montar(docs: list[dict]) -> list[LembreteVesperaResponse]:
    servicos = await _mapa(db.servicos, [d["servico_id"] for d in docs])
    clientes = await _mapa(db.clientes, [d["cliente_id"] for d in docs])
    profs = await _mapa(db.profissionais, [d["profissional_id"] for d in docs])
    itens = []
    for d in docs:
        cliente = clientes.get(d["cliente_id"], {})
        telefone = cliente.get("telefone") or ""
        itens.append(
            LembreteVesperaResponse.from_mongo(
                {
                    **d,
                    "cliente_nome": cliente.get("nome"),
                    "cliente_telefone": telefone,
                    "telefone_e164": normalizar_telefone(telefone),
                    "servico_nome": servicos.get(d["servico_id"], {}).get("nome", "—"),
                    "profissional_nome": profs.get(d["profissional_id"], {}).get("nome", "—"),
                    "lembrete": d.get("lembrete") or {},
                }
            )
        )
    return itens


async def listar_amanha(ids: list[str] | None = None) -> list[LembreteVesperaResponse]:
    inicio, fim = janela_dia(1)
    filtro: dict = {"data_hora_inicio": {"$gte": inicio, "$lt": fim}, "status": {"$in": list(STATUS_ATIVOS)}}
    if ids:
        filtro["_id"] = {"$in": [oid(i) for i in ids]}
    docs = await db.agendamentos.find(filtro).sort("data_hora_inicio", 1).to_list(200)
    return await _montar(docs)


async def obter(agendamento_id: str) -> LembreteVesperaResponse:
    doc = await db.agendamentos.find_one({"_id": oid(agendamento_id, "Agendamento não encontrado")})
    if doc is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return (await _montar([doc]))[0]


async def salvar_mensagem(agendamento_id: str, mensagem: str) -> LembreteVesperaResponse:
    doc = await db.agendamentos.find_one_and_update(
        {"_id": oid(agendamento_id, "Agendamento não encontrado")},
        {"$set": {"lembrete.mensagem": mensagem.strip(), "lembrete.gerado_em": now()}},
        return_document=ReturnDocument.AFTER,
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return (await _montar([doc]))[0]


async def registrar_envio(item: LembreteVesperaResponse, canal: str, mensagem: str, twilio_sid: str | None = None):
    campos = {"lembrete.enviado_em": now(), "lembrete.canal": canal, "lembrete.twilio_sid": twilio_sid, "lembrete.erro": None}
    doc = await db.agendamentos.find_one_and_update(
        {"_id": ObjectId(item.id)}, {"$set": campos}, return_document=ReturnDocument.AFTER
    )
    await db.lembretes.insert_one(
        {
            "mensagem": mensagem,
            "canal": f"{canal}:{item.telefone_e164 or item.cliente_telefone}",
            "criado_em": now(),
            "agendamento_id": ObjectId(item.id),
            "salao_id": 1,
        }
    )
    return (await _montar([doc]))[0]


async def registrar_erro(item: LembreteVesperaResponse, erro: str) -> LembreteVesperaResponse:
    doc = await db.agendamentos.find_one_and_update(
        {"_id": ObjectId(item.id)}, {"$set": {"lembrete.erro": erro}}, return_document=ReturnDocument.AFTER
    )
    return (await _montar([doc]))[0]
