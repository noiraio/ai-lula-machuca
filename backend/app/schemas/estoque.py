from pydantic import BaseModel


class AlertaEstoqueResponse(BaseModel):
    insumo_id: str
    nome: str
    quantidade_atual: int
    quantidade_minima_alerta: int
    demanda_prevista: float
    tipo: str
    mensagem: str
