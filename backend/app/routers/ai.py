import asyncio
import json
import logging
from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.db import db, local, now
from app.dependencies import get_current_user
from app.schemas.ai import ChatMessage, ChatRequest, GerarMensagemRequest
from app.schemas.lembrete import LembretesVesperaIARequest
from app.schemas.usuario import UsuarioResponse
from app.services import ai
from app.services import lembretes as lembretes_service

router = APIRouter(prefix="/ai", tags=["ai"])
logger = logging.getLogger("elo.ai")

SSE_HEADERS = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
CONCORRENCIA_IA = 3


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


async def _stream(chat, texto: str, meta: dict, ao_final=None):
    yield _sse(meta)
    partes: list[str] = []
    try:
        async for delta in ai.stream_texto(chat, texto):
            partes.append(delta)
            yield _sse({"delta": delta})
    except Exception:  # noqa: BLE001
        logger.exception("Falha na IA")
        yield _sse({"error": "O assistente não conseguiu responder agora. Tente novamente."})
    if partes and ao_final:
        await ao_final("".join(partes))
    yield _sse({"done": True})


@router.get("/chat/{session_id}/messages", response_model=list[ChatMessage])
async def historico(session_id: str, user: UsuarioResponse = Depends(get_current_user)):
    docs = await db.chat_messages.find({"session_id": session_id, "user_id": user.id}).sort("criado_em", 1).to_list(200)
    return [ChatMessage.from_mongo(d) for d in docs]


@router.post("/chat")
async def chat(body: ChatRequest, user: UsuarioResponse = Depends(get_current_user)):
    session_id = body.session_id or uuid4().hex
    historico_docs = await db.chat_messages.find({"session_id": session_id, "user_id": user.id}).sort("criado_em", 1).to_list(60)
    historico = [{"role": m["role"], "content": m["content"]} for m in historico_docs]

    system = await ai.contexto_salao(user)
    llm = ai.novo_chat(session_id, system, historico)

    await db.chat_messages.insert_one(
        {"session_id": session_id, "user_id": user.id, "role": "user", "content": body.message, "criado_em": now()}
    )

    async def salvar_resposta(texto: str):
        await db.chat_messages.insert_one(
            {"session_id": session_id, "user_id": user.id, "role": "assistant", "content": texto, "criado_em": now()}
        )

    return StreamingResponse(
        _stream(llm, body.message, {"session_id": session_id}, salvar_resposta),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


@router.post("/gerar-mensagem")
async def gerar_mensagem(body: GerarMensagemRequest, user: UsuarioResponse = Depends(get_current_user)):
    system, pedido = ai.prompt_mensagem_whatsapp(
        user, body.tom, cliente_nome=body.cliente_nome, servico=body.servico, horario=body.horario
    )
    llm = ai.novo_chat(f"msg-{uuid4().hex}", system)
    return StreamingResponse(_stream(llm, pedido, {"tipo": "mensagem"}), media_type="text/event-stream", headers=SSE_HEADERS)


@router.post("/lembretes-vespera")
async def gerar_lembretes_vespera(body: LembretesVesperaIARequest, user: UsuarioResponse = Depends(get_current_user)):
    """Gera (em paralelo, com streaming de progresso) uma mensagem personalizada por agendamento de amanhã."""
    itens = await lembretes_service.listar_amanha(body.agendamento_ids)
    semaforo = asyncio.Semaphore(CONCORRENCIA_IA)

    async def gerar(item):
        async with semaforo:
            system, pedido = ai.prompt_mensagem_whatsapp(
                user,
                body.tom,
                cliente_nome=item.cliente_nome,
                servico=item.servico_nome,
                horario=f"amanhã às {local(item.data_hora_inicio).strftime('%H:%M')}",
                profissional=item.profissional_nome,
                vespera=True,
            )
            texto = await ai.gerar_texto(f"vespera-{item.id}-{uuid4().hex[:6]}", system, pedido)
            await lembretes_service.salvar_mensagem(item.id, texto)
            return item.id, texto

    async def progresso():
        yield _sse({"total": len(itens)})
        tarefas = {asyncio.ensure_future(gerar(i)): i.id for i in itens}
        for fut in asyncio.as_completed(tarefas):
            try:
                agendamento_id, texto = await fut
                yield _sse({"agendamento_id": agendamento_id, "mensagem": texto})
            except Exception:  # noqa: BLE001
                logger.exception("Falha ao gerar lembrete de véspera")
                yield _sse({"falha": "Não foi possível gerar uma das mensagens."})
        yield _sse({"done": True})

    return StreamingResponse(progresso(), media_type="text/event-stream", headers=SSE_HEADERS)
