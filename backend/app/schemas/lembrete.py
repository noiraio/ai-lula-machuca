from datetime import datetime

from pydantic import BaseModel

from app.db import BaseDocument


class LembreteCreate(BaseModel):
    mensagem: str
    canal: str


class LembreteResponse(BaseDocument):
    mensagem: str
    canal: str
    criado_em: datetime
