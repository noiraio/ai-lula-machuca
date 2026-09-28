from datetime import timedelta

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pymongo import ReturnDocument

from app import config
from app.db import db, now, oid
from app.dependencies import extrair_token, get_current_user
from app.schemas.usuario import (
    LoginRequest,
    RegisterRequest,
    SessionRequest,
    SessionResponse,
    TokenResponse,
    UsuarioResponse,
    UsuarioUpdate,
)
from app.services.auth import autenticar_usuario, criar_token, hash_senha

router = APIRouter(prefix="/auth", tags=["auth"])

COOKIE = dict(key="session_token", httponly=True, secure=True, samesite="none", path="/")


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    user = await autenticar_usuario(body.email, body.senha)
    if user is None:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return TokenResponse(access_token=criar_token(str(user["_id"])))


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(body: RegisterRequest):
    email = body.email.lower().strip()
    if await db.usuarios.find_one({"email": email}):
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    if len(body.senha) < 6:
        raise HTTPException(status_code=422, detail="A senha precisa ter pelo menos 6 caracteres")
    res = await db.usuarios.insert_one(
        {
            "email": email,
            "senha_hash": hash_senha(body.senha),
            "nome": body.nome.strip(),
            "business": body.business,
            "city": None,
            "picture": None,
            "criado_em": now(),
        }
    )
    return TokenResponse(access_token=criar_token(str(res.inserted_id)))


@router.post("/session", response_model=SessionResponse)
async def session(body: SessionRequest, response: Response):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(config.EMERGENT_AUTH_SESSION_URL, headers={"X-Session-ID": body.session_id})
    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Sessão do Google inválida ou expirada")
    dados = r.json()
    email = dados["email"].lower().strip()

    user = await db.usuarios.find_one_and_update(
        {"email": email},
        {
            "$set": {"picture": dados.get("picture")},
            "$setOnInsert": {
                "email": email,
                "nome": dados.get("name") or email.split("@")[0],
                "business": None,
                "city": None,
                "criado_em": now(),
            },
        },
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )

    session_token = dados["session_token"]
    expires_at = now() + timedelta(days=config.SESSION_DAYS)
    await db.user_sessions.insert_one(
        {"user_id": str(user["_id"]), "session_token": session_token, "expires_at": expires_at, "created_at": now()}
    )
    response.set_cookie(value=session_token, max_age=config.SESSION_DAYS * 24 * 3600, **COOKIE)
    return SessionResponse(access_token=session_token, user=UsuarioResponse.from_mongo(user))


@router.post("/logout", status_code=204)
async def logout(request: Request, response: Response):
    token = extrair_token(request)
    if token:
        await db.user_sessions.delete_one({"session_token": token})
    response.delete_cookie(key="session_token", path="/", secure=True, samesite="none")


@router.get("/me", response_model=UsuarioResponse)
async def me(user: UsuarioResponse = Depends(get_current_user)):
    return user


@router.put("/me", response_model=UsuarioResponse)
async def atualizar_perfil(body: UsuarioUpdate, user: UsuarioResponse = Depends(get_current_user)):
    campos = body.model_dump(exclude_unset=True, exclude_none=True)
    if "email" in campos:
        campos["email"] = campos["email"].lower().strip()
        outro = await db.usuarios.find_one({"email": campos["email"], "_id": {"$ne": oid(user.id)}})
        if outro:
            raise HTTPException(status_code=409, detail="E-mail já em uso")
    if not campos:
        return user
    doc = await db.usuarios.find_one_and_update(
        {"_id": oid(user.id)}, {"$set": campos}, return_document=ReturnDocument.AFTER
    )
    return UsuarioResponse.from_mongo(doc)
