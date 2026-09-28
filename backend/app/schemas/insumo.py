from pydantic import BaseModel

from app.db import BaseDocument


class InsumoCreate(BaseModel):
    nome: str
    quantidade_atual: float = 0
    quantidade_minima_alerta: float = 0


class InsumoUpdate(BaseModel):
    nome: str | None = None
    quantidade_atual: float | None = None
    quantidade_minima_alerta: float | None = None


class InsumoResponse(BaseDocument):
    nome: str
    quantidade_atual: float
    quantidade_minima_alerta: float
