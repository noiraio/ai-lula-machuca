from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, Request
from jose import JWTError, jwt

from app import config
from app.db import db, now, utc
from app.schemas.usuario import UsuarioResponse


def extrair_token(request: Request) -> str | None:
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth[7:].strip()
    return request.cookies.get("session_token")


async def _user_por_jwt(token: str) -> dict | None:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.JWT_ALGORITHM])
        return await db.usuarios.find_one({"_id": ObjectId(payload["sub"])})
    except (JWTError, KeyError, InvalidId, TypeError):
        return None


async def _user_por_sessao(token: str) -> dict | None:
    sessao = await db.user_sessions.find_one({"session_token": token})
    if sessao is None or utc(sessao["expires_at"]) < now():
        return None
    return await db.usuarios.find_one({"_id": ObjectId(sessao["user_id"])})


async def get_current_user(request: Request) -> UsuarioResponse:
    token = extrair_token(request)
    if not token:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = await _user_por_jwt(token) or await _user_por_sessao(token)
    if user is None:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return UsuarioResponse.from_mongo(user)
