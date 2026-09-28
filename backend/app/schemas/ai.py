from datetime import datetime

from pydantic import BaseModel, Field

from app.db import BaseDocument


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None


class ChatMessage(BaseDocument):
    session_id: str
    role: str
    content: str
    criado_em: datetime


class GerarMensagemRequest(BaseModel):
    cliente_nome: str | None = None
    servico: str | None = None
    horario: str | None = None
    tom: str = "carinhoso e profissional"
