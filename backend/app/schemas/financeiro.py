from datetime import datetime

from pydantic import BaseModel

from app.db import BaseDocument


class FaturamentoResponse(BaseModel):
    total: float
    data_inicio: str
    data_fim: str


class MovimentoCreate(BaseModel):
    tipo: str
    valor: float
    descricao: str


class MovimentoResponse(BaseDocument):
    tipo: str
    valor: float
    descricao: str
    data: datetime


class ResumoFinanceiroResponse(BaseModel):
    entradas: float
    saidas: float
    saldo: float
    lancamentos: list[MovimentoResponse]
