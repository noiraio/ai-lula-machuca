from pydantic import BaseModel

from app.db import BaseDocument


class ProfissionalCreate(BaseModel):
    nome: str
    especialidades: str | None = None


class ProfissionalUpdate(BaseModel):
    nome: str | None = None
    especialidades: str | None = None


class ProfissionalResponse(BaseDocument):
    nome: str
    especialidades: str | None = None
