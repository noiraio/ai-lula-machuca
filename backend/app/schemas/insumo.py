from pydantic import BaseModel

from app.db import BaseDocument


class InsumoCreate(BaseModel):
    nome: str
    quantidade_atual: int = 0
    quantidade_minima_alerta: int = 0


class InsumoUpdate(BaseModel):
    nome: str | None = None
    quantidade_atual: int | None = None
    quantidade_minima_alerta: int | None = None


class InsumoResponse(BaseDocument):
    nome: str
    quantidade_atual: int
    quantidade_minima_alerta: int
