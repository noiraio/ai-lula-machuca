"""Envio de WhatsApp via Twilio (REST API, sem SDK).

Ativa automaticamente quando TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN e
TWILIO_WHATSAPP_FROM estiverem preenchidos no backend/.env.
Sem credenciais, o app continua funcionando com links wa.me.
"""

import re
from urllib.parse import quote

import httpx

from app import config

SANDBOX_FROM = "whatsapp:+14155238886"
TWILIO_API = "https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"


class EnvioWhatsAppError(Exception):
    pass


def configurado() -> bool:
    return bool(config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN and config.TWILIO_WHATSAPP_FROM)


def usando_sandbox() -> bool:
    return config.TWILIO_WHATSAPP_FROM == SANDBOX_FROM


def remetente_mascarado() -> str | None:
    if not config.TWILIO_WHATSAPP_FROM:
        return None
    numero = config.TWILIO_WHATSAPP_FROM.replace("whatsapp:", "")
    return f"{numero[:4]}…{numero[-4:]}" if len(numero) > 8 else numero


def normalizar_telefone(telefone: str | None) -> str | None:
    """Converte '55 42 99999-0000', '(42) 99999-0000' ou '5542999990000' para E.164 (+5542999990000)."""
    digitos = re.sub(r"\D", "", telefone or "")
    if not digitos:
        return None
    if len(digitos) in (10, 11):
        digitos = "55" + digitos
    if not 12 <= len(digitos) <= 15:
        return None
    return "+" + digitos


def link_wa(telefone_e164: str, mensagem: str) -> str:
    return f"https://wa.me/{telefone_e164.lstrip('+')}?text={quote(mensagem)}"


async def enviar(telefone_e164: str, mensagem: str) -> str:
    """Envia a mensagem e devolve o SID do Twilio."""
    if not configurado():
        raise EnvioWhatsAppError("Twilio não configurado. Preencha TWILIO_* no backend/.env.")
    url = TWILIO_API.format(sid=config.TWILIO_ACCOUNT_SID)
    payload = {"From": config.TWILIO_WHATSAPP_FROM, "To": f"whatsapp:{telefone_e164}", "Body": mensagem}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(url, auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN), data=payload)
    except httpx.HTTPError as exc:
        raise EnvioWhatsAppError(f"Falha de rede ao contatar o Twilio: {exc}") from exc
    if r.status_code >= 400:
        try:
            detalhe = r.json().get("message")
        except ValueError:
            detalhe = r.text
        raise EnvioWhatsAppError(detalhe or f"Twilio respondeu HTTP {r.status_code}")
    return r.json()["sid"]
