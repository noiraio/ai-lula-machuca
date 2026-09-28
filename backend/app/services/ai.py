from datetime import timedelta
from typing import AsyncIterator

from emergentintegrations.llm.chat import LlmChat, StreamDone, TextDelta, UserMessage

from app import config
from app.db import db, now, utc

PROVIDER = "anthropic"
MODEL = "claude-sonnet-4-5-20250929"


def novo_chat(session_id: str, system_message: str, historico: list[dict] | None = None) -> LlmChat:
    initial = [{"role": "system", "content": system_message}, *(historico or [])]
    return LlmChat(
        api_key=config.EMERGENT_LLM_KEY,
        session_id=session_id,
        system_message=system_message,
        initial_messages=initial,
    ).with_model(PROVIDER, MODEL)


async def stream_texto(chat: LlmChat, texto: str) -> AsyncIterator[str]:
    async for ev in chat.stream_message(UserMessage(text=texto)):
        if isinstance(ev, TextDelta):
            yield ev.content
        elif isinstance(ev, StreamDone):
            break


async def contexto_salao(user) -> str:
    hoje = now().replace(hour=0, minute=0, second=0, microsecond=0)
    amanha = hoje + timedelta(days=1)

    servicos = await db.servicos.find().to_list(50)
    profissionais = await db.profissionais.find().to_list(50)
    insumos = await db.insumos.find().to_list(100)
    agendamentos = await db.agendamentos.find(
        {"data_hora_inicio": {"$gte": hoje, "$lt": amanha}}
    ).sort("data_hora_inicio", 1).to_list(50)

    srv_map = {s["_id"]: s for s in servicos}
    prof_map = {p["_id"]: p for p in profissionais}
    cli_ids = [a["cliente_id"] for a in agendamentos]
    clientes = {c["_id"]: c for c in await db.clientes.find({"_id": {"$in": cli_ids}}).to_list(50)} if cli_ids else {}

    linhas_ag = [
        f"- {utc(a['data_hora_inicio']).strftime('%H:%M')} UTC — "
        f"{clientes.get(a['cliente_id'], {}).get('nome') or 'Cliente'} · "
        f"{srv_map.get(a['servico_id'], {}).get('nome', '?')} com "
        f"{prof_map.get(a['profissional_id'], {}).get('nome', '?')} ({a['status']})"
        for a in agendamentos
    ] or ["- nenhum agendamento hoje"]
    linhas_srv = [f"- {s['nome']}: {s['duracao_minutos']} min, R$ {s['valor']:.2f}" for s in servicos] or ["- nenhum"]
    linhas_prof = [f"- {p['nome']} ({p.get('especialidades') or 'geral'})" for p in profissionais] or ["- nenhum"]
    baixos = [
        f"- {i['nome']}: {i['quantidade_atual']} un (mínimo {i['quantidade_minima_alerta']})"
        for i in insumos
        if i["quantidade_atual"] <= i["quantidade_minima_alerta"]
    ] or ["- tudo em dia"]

    return (
        "Você é o Assistente ELO, a inteligência do sistema de gestão ELO Beauty Care para salões de beleza. "
        f"Você conversa com {user.nome}, responsável pelo espaço \"{user.business or 'ELO Beauty Care'}\""
        f"{' em ' + user.city if user.city else ''}. "
        "Seja acolhedor, direto e prático. Responda sempre em português do Brasil, em frases curtas, "
        "sem markdown pesado (pode usar listas simples com '-'). Ajude com agenda, atendimento ao cliente, "
        "mensagens para WhatsApp, estoque, finanças e organização do salão. "
        "Use os dados abaixo quando forem relevantes; se não souber algo, diga que não tem a informação.\n\n"
        f"AGENDA DE HOJE:\n" + "\n".join(linhas_ag) + "\n\n"
        f"SERVIÇOS OFERECIDOS:\n" + "\n".join(linhas_srv) + "\n\n"
        f"EQUIPE:\n" + "\n".join(linhas_prof) + "\n\n"
        f"INSUMOS COM ESTOQUE BAIXO:\n" + "\n".join(baixos)
    )


def prompt_mensagem_whatsapp(body, user) -> tuple[str, str]:
    system = (
        "Você redige mensagens curtas de WhatsApp para clientes de um salão de beleza chamado "
        f"\"{user.business or 'ELO Beauty Care'}\". Escreva em português do Brasil, em primeira pessoa do salão, "
        "com no máximo 3 frases, tom {tom}, no máximo 1 emoji. Responda APENAS com o texto da mensagem, "
        "sem aspas, sem explicações."
    ).format(tom=body.tom)
    detalhes = []
    if body.cliente_nome:
        detalhes.append(f"nome da cliente: {body.cliente_nome}")
    if body.servico:
        detalhes.append(f"serviço: {body.servico}")
    if body.horario:
        detalhes.append(f"horário: {body.horario}")
    pedido = "Escreva um lembrete de atendimento pedindo confirmação de presença."
    if detalhes:
        pedido += " Detalhes: " + "; ".join(detalhes) + "."
    return system, pedido
