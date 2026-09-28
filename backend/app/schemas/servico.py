from pydantic import BaseModel

from app.db import BaseDocument


class ServicoCreate(BaseModel):
    nome: str
    duracao_minutos: int
    valor: float


class ServicoUpdate(BaseModel):
    nome: str | None = None
    duracao_minutos: int | None = None
    valor: float | None = None


class ServicoResponse(BaseDocument):
    nome: str
    duracao_minutos: int
    valor: float
