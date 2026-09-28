from pydantic import BaseModel


class AlertaEstoqueResponse(BaseModel):
    insumo_id: str
    nome: str
    quantidade_atual: float
    quantidade_minima_alerta: float
    demanda_prevista: float
    tipo: str
    mensagem: str
