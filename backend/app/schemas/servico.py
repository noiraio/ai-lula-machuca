from pydantic import BaseModel, Field

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


class ServicoInsumoCreate(BaseModel):
    insumo_id: str
    quantidade_utilizada: float = Field(gt=0)


class ServicoInsumoResponse(BaseDocument):
    servico_id: str
    insumo_id: str
    insumo_nome: str = "—"
    quantidade_utilizada: float
    quantidade_atual: float = 0
    quantidade_minima_alerta: float = 0
