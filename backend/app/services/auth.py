from datetime import timedelta

import bcrypt
from jose import jwt

from app import config
from app.db import db, now


def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


def verificar_senha(senha: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(senha.encode(), senha_hash.encode())


def criar_token(user_id: str) -> str:
    expire = now() + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": user_id, "exp": expire}, config.SECRET_KEY, algorithm=config.JWT_ALGORITHM)


async def autenticar_usuario(email: str, senha: str) -> dict | None:
    user = await db.usuarios.find_one({"email": email.lower().strip()})
    if user is None or not user.get("senha_hash") or not verificar_senha(senha, user["senha_hash"]):
        return None
    return user
