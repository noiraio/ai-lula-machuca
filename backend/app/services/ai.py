from typing import AsyncIterator

from emergentintegrations.llm.chat import LlmChat, StreamDone, TextDelta, UserMessage

from app import config
from app.db import db, janela_dia, local

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


async def gerar_texto(session_id: str, system_message: str, pedido: str) -> str:
    chat = novo_chat(session_id, system_message)
    return "".join([parte async for parte in stream_texto(chat, pedido)]).strip()


async def contexto_salao(user) -> str:
    hoje, amanha = janela_dia(0)

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
        f"- {local(a['data_hora_inicio']).strftime('%H:%M')} — "
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
        f"Hoje é {hoje.strftime('%d/%m/%Y')} (fuso {config.TIMEZONE}); horários abaixo já estão no horário local. "
        "Seja acolhedor, direto e prático. Responda sempre em português do Brasil, em frases curtas, "
        "sem markdown pesado (pode usar listas simples com '-'). Ajude com agenda, atendimento ao cliente, "
        "mensagens para WhatsApp, estoque, finanças e organização do salão. "
        "Use os dados abaixo quando forem relevantes; se não souber algo, diga que não tem a informação.\n\n"
        f"AGENDA DE HOJE:\n" + "\n".join(linhas_ag) + "\n\n"
        f"SERVIÇOS OFERECIDOS:\n" + "\n".join(linhas_srv) + "\n\n"
        f"EQUIPE:\n" + "\n".join(linhas_prof) + "\n\n"
        f"INSUMOS COM ESTOQUE BAIXO:\n" + "\n".join(baixos)
    )


def prompt_mensagem_whatsapp(
    user,
    tom: str,
    *,
    cliente_nome: str | None = None,
    servico: str | None = None,
    horario: str | None = None,
    profissional: str | None = None,
    vespera: bool = False,
) -> tuple[str, str]:
    system = (
        "Você redige mensagens curtas de WhatsApp para clientes de um salão de beleza chamado "
        f"\"{user.business or 'ELO Beauty Care'}\". Escreva em português do Brasil, em primeira pessoa do salão, "
        f"com no máximo 3 frases, tom {tom}, no máximo 1 emoji. Responda APENAS com o texto da mensagem, "
        "sem aspas, sem explicações, sem assinatura."
    )
    detalhes = [
        f"nome da cliente: {cliente_nome}" if cliente_nome else None,
        f"serviço: {servico}" if servico else None,
        f"horário: {horario}" if horario else None,
        f"profissional que vai atender: {profissional}" if profissional else None,
    ]
    pedido = (
        "Escreva um lembrete de véspera: o atendimento é AMANHÃ. Peça para a cliente confirmar presença respondendo a mensagem."
        if vespera
        else "Escreva um lembrete de atendimento pedindo confirmação de presença."
    )
    if any(detalhes):
        pedido += " Detalhes: " + "; ".join(d for d in detalhes if d) + "."
    return system, pedido
