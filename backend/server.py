"""ELO Beauty Care — entrypoint (FastAPI + MongoDB via Motor)."""

import logging
from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import config
from app.db import db, now
from app.routers import (
    agendamentos,
    ai,
    auth,
    dashboard,
    debitos,
    estoque,
    financeiro,
    insumos,
    lembretes,
    profissionais,
    servicos,
)
from app.services.auth import hash_senha

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("elo-beauty-care")

ADMIN_EMAIL = "admin@elo.beauty"
ADMIN_SENHA = "elo123456"


async def _criar_indices() -> None:
    await db.usuarios.create_index("email", unique=True)
    await db.clientes.create_index("telefone", unique=True)
    await db.user_sessions.create_index("session_token", unique=True)
    await db.user_sessions.create_index("expires_at", expireAfterSeconds=0)
    await db.agendamentos.create_index([("profissional_id", 1), ("data_hora_inicio", 1)])
    await db.chat_messages.create_index([("session_id", 1), ("criado_em", 1)])


async def _seed_demo() -> None:
    if await db.usuarios.count_documents({"email": ADMIN_EMAIL}) == 0:
        await db.usuarios.insert_one(
            {
                "email": ADMIN_EMAIL,
                "senha_hash": hash_senha(ADMIN_SENHA),
                "nome": "Admin ELO",
                "business": "ELO Beauty Care",
                "city": "São Paulo",
                "picture": None,
                "criado_em": now(),
            }
        )

    if await db.servicos.count_documents({}) == 0:
        await db.servicos.insert_many(
            [
                {"nome": "Corte Feminino", "duracao_minutos": 45, "valor": 120.0, "salao_id": 1},
                {"nome": "Escova", "duracao_minutos": 40, "valor": 90.0, "salao_id": 1},
                {"nome": "Coloração", "duracao_minutos": 90, "valor": 220.0, "salao_id": 1},
                {"nome": "Manicure", "duracao_minutos": 45, "valor": 60.0, "salao_id": 1},
                {"nome": "Design de Sobrancelhas", "duracao_minutos": 30, "valor": 55.0, "salao_id": 1},
            ]
        )

    if await db.profissionais.count_documents({}) == 0:
        await db.profissionais.insert_many(
            [
                {"nome": "Carla Nunes", "especialidades": "Cabelo, Coloração", "salao_id": 1},
                {"nome": "Renata Lima", "especialidades": "Unhas, Sobrancelhas", "salao_id": 1},
            ]
        )

    if await db.insumos.count_documents({}) == 0:
        await db.insumos.insert_many(
            [
                {"nome": "Shampoo Profissional", "quantidade_atual": 24, "quantidade_minima_alerta": 8, "salao_id": 1},
                {"nome": "Coloração Loiro", "quantidade_atual": 6, "quantidade_minima_alerta": 5, "salao_id": 1},
                {"nome": "Máscara Hidratante", "quantidade_atual": 18, "quantidade_minima_alerta": 6, "salao_id": 1},
                {"nome": "Esmalte Rosa", "quantidade_atual": 3, "quantidade_minima_alerta": 4, "salao_id": 1},
            ]
        )

    if await db.clientes.count_documents({}) == 0:
        await db.clientes.insert_many(
            [
                {"telefone": "5511990000001", "nome": "Amanda Martins"},
                {"telefone": "5511990000002", "nome": "João Costa"},
                {"telefone": "5511990000003", "nome": "Beatriz Rocha"},
            ]
        )

    if await db.agendamentos.count_documents({}) == 0:
        clientes = await db.clientes.find().sort("_id", 1).to_list(10)
        servicos_lst = await db.servicos.find().sort("_id", 1).to_list(10)
        profs = await db.profissionais.find().sort("_id", 1).to_list(10)
        hoje = now().replace(hour=0, minute=0, second=0, microsecond=0)
        base = [(0, 13, 0, 0, 0), (0, 17, 1, 1, 0), (1, 12, 2, 3, 1), (1, 18, 0, 2, 0), (2, 14, 1, 0, 0)]
        docs = []
        for delta_days, hora, ci, si, pi in base:
            inicio = hoje + timedelta(days=delta_days, hours=hora)
            docs.append(
                {
                    "cliente_id": clientes[ci]["_id"],
                    "profissional_id": profs[pi]["_id"],
                    "servico_id": servicos_lst[si]["_id"],
                    "data_hora_inicio": inicio,
                    "data_hora_fim": inicio + timedelta(minutes=servicos_lst[si]["duracao_minutos"]),
                    "status": "confirmado",
                    "salao_id": 1,
                }
            )
        await db.agendamentos.insert_many(docs)

    if await db.movimentos_financeiros.count_documents({}) == 0:
        await db.movimentos_financeiros.insert_many(
            [
                {"tipo": "entrada", "valor": 340.0, "descricao": "Atendimentos do dia", "data": now(), "salao_id": 1},
                {"tipo": "entrada", "valor": 220.0, "descricao": "Coloração — Amanda", "data": now(), "salao_id": 1},
                {"tipo": "saida", "valor": 180.0, "descricao": "Compra de insumos", "data": now(), "salao_id": 1},
            ]
        )


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: D401
    logger.info("Conectando ao MongoDB (%s)...", config.DB_NAME)
    try:
        await _criar_indices()
        await _seed_demo()
    except Exception:  # noqa: BLE001
        logger.exception("Falha ao preparar banco/dados demo")
    logger.info("Backend pronto.")
    yield


app = FastAPI(title="ELO Beauty Care API", lifespan=lifespan)

_origins = [o.strip() for o in config.CORS_ORIGINS.split(",") if o.strip()]
if _origins == ["*"]:
    app.add_middleware(
        CORSMiddleware, allow_origin_regex=".*", allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )
else:
    app.add_middleware(
        CORSMiddleware, allow_origins=_origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
    )

api = APIRouter(prefix="/api")
for r in (auth, agendamentos, servicos, insumos, profissionais, dashboard, estoque, financeiro, debitos, lembretes, ai):
    api.include_router(r.router)


@api.get("/health")
async def health():
    return {"status": "ok", "app": "ELO Beauty Care", "db": config.DB_NAME}


app.include_router(api)
