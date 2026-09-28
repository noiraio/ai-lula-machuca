from pydantic import BaseModel

from app.db import BaseDocument


class DebitoCreate(BaseModel):
    cliente_nome: str
    descricao: str
    valor: float


class DebitoResponse(BaseDocument):
    cliente_nome: str
    descricao: str
    valor: float
