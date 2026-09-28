from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.db import BaseDocument


class LoginRequest(BaseModel):
    email: str
    senha: str


class RegisterRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    business: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class SessionRequest(BaseModel):
    session_id: str


class UsuarioResponse(BaseDocument):
    email: str
    nome: str
    business: str | None = None
    city: str | None = None
    picture: str | None = None
    criado_em: datetime | None = None


class SessionResponse(TokenResponse):
    user: UsuarioResponse


class UsuarioUpdate(BaseModel):
    nome: str | None = None
    business: str | None = None
    city: str | None = None
    email: str | None = None
