from datetime import datetime

from pydantic import BaseModel

from app.db import BaseDocument


class AgendamentoResponse(BaseDocument):
    cliente_id: str
    profissional_id: str
    servico_id: str
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: str
    servico_nome: str = "—"
    cliente_nome: str | None = None
    profissional_nome: str = "—"
    servico_valor: float = 0.0
    alertas_estoque: list[str] = []


class AgendamentoCreate(BaseModel):
    servico_id: str
    profissional_id: str
    cliente_telefone: str
    cliente_nome: str | None = None
    cliente_id: str | None = None
    data_hora_inicio: datetime
    data_hora_fim: datetime | None = None


class AgendamentoUpdate(BaseModel):
    servico_id: str | None = None
    profissional_id: str | None = None
    cliente_id: str | None = None
    data_hora_inicio: datetime | None = None
    data_hora_fim: datetime | None = None
    status: str | None = None
