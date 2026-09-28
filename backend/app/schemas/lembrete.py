from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.db import BaseDocument, MongoModel


class LembreteCreate(BaseModel):
    mensagem: str
    canal: str


class LembreteResponse(BaseDocument):
    mensagem: str
    canal: str
    criado_em: datetime


class LembreteInfo(MongoModel):
    mensagem: str | None = None
    gerado_em: datetime | None = None
    enviado_em: datetime | None = None
    canal: str | None = None
    twilio_sid: str | None = None
    erro: str | None = None


class LembreteVesperaResponse(BaseDocument):
    cliente_nome: str | None = None
    cliente_telefone: str
    telefone_e164: str | None = None
    servico_nome: str
    profissional_nome: str
    data_hora_inicio: datetime
    status: str
    lembrete: LembreteInfo = LembreteInfo()


class LembreteMensagemUpdate(BaseModel):
    mensagem: str = Field(min_length=1, max_length=1000)


class EnviarLembreteRequest(BaseModel):
    canal: Literal["twilio", "whatsapp_link"] = "twilio"
    mensagem: str | None = None


class EnvioResultado(BaseModel):
    agendamento_id: str
    ok: bool
    detalhe: str | None = None
    item: LembreteVesperaResponse | None = None


class WhatsAppConfigResponse(BaseModel):
    twilio_configurado: bool
    sandbox: bool
    remetente: str | None = None


class LembretesVesperaIARequest(BaseModel):
    agendamento_ids: list[str] | None = None
    tom: str = "carinhoso e profissional"
