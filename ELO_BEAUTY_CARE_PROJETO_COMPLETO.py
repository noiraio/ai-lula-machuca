#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ELO BEAUTY CARE — PROJETO COMPLETO EM UM ÚNICO ARQUIVO
======================================================
React (frontend) + FastAPI (backend) + MongoDB + IA Claude Sonnet 4.5 + Google Auth + WhatsApp.

COMO USAR
---------
1. Salve este arquivo em qualquer pasta do seu computador.
2. Abra um terminal nessa pasta e rode:

       python ELO_BEAUTY_CARE_PROJETO_COMPLETO.py

   (opcional: informe a pasta de destino →  python ELO_BEAUTY_CARE_PROJETO_COMPLETO.py minha-pasta)

3. A pasta  elo-beauty-care/  será criada com toda a estrutura (126 arquivos):
       backend/   frontend/   .vscode/   README.md   INTEGRACAO_WHATSAPP.md ...
4. Abra a pasta no VS Code e siga o README.md ("Rodando no VS Code (local)").

Cada arquivo do projeto aparece abaixo, na íntegra, precedido de uma linha
"===== FILE: caminho/do/arquivo =====" — você também pode ler/copiar direto daqui.
"""

import sys
from pathlib import Path

MARCADOR = "===== FILE: "
DESTINO_PADRAO = "elo-beauty-care"


def extrair(destino: Path) -> int:
    blocos = ARQUIVOS.split(MARCADOR)[1:]
    for bloco in blocos:
        cabecalho, _, conteudo = bloco.partition("\n")
        caminho_rel = cabecalho.replace("=====", "").strip()
        if conteudo.endswith("\n"):
            conteudo = conteudo[:-1]  # remove o separador entre arquivos
        alvo = destino / caminho_rel
        alvo.parent.mkdir(parents=True, exist_ok=True)
        alvo.write_text(conteudo, encoding="utf-8")
        print("  +", caminho_rel)
    return len(blocos)


def main() -> None:
    destino = Path(sys.argv[1] if len(sys.argv) > 1 else DESTINO_PADRAO).resolve()
    if destino.exists() and any(destino.iterdir()):
        resposta = input(f"A pasta {destino} já existe e não está vazia. Sobrescrever arquivos? [s/N] ")
        if resposta.strip().lower() not in ("s", "sim", "y", "yes"):
            print("Cancelado.")
            return
    destino.mkdir(parents=True, exist_ok=True)
    print(f"Extraindo para {destino} ...")
    n = extrair(destino)
    print(f"\nPronto! {n} arquivos criados.")
    print("Próximos passos:")
    print(f"  1. cd {destino}")
    print("  2. Copie backend/.env.example → backend/.env e frontend/.env.example → frontend/.env e preencha")
    print("  3. Siga o README.md para instalar dependências e rodar backend (8001) e frontend (3000)")


ARQUIVOS = r'''
===== FILE: README.md =====
# ELO Beauty Care

Sistema de gestão para salões de beleza — **React** (frontend) + **FastAPI** (backend) + **MongoDB**, com IA (**Claude Sonnet 4.5**), login por e-mail/senha (JWT) e **Google**, e lembretes de véspera por WhatsApp (wa.me ou Twilio).

## Estrutura do projeto

```
elo-beauty-care/
├── README.md                     ← este guia
├── INTEGRACAO_WHATSAPP.md        ← lembretes de véspera + como ativar o Twilio
├── auth_testing.md               ← como testar o login Google sem navegador
├── .vscode/                      ← launch/settings/extensions prontos para o VS Code
│
├── backend/                      ← API FastAPI (porta 8001)
│   ├── server.py                 ← entrypoint: app, CORS, índices, seed de dados demo, rotas /api/*
│   ├── requirements.txt
│   ├── .env                      ← variáveis (veja .env.example)
│   ├── .env.example
│   ├── pytest.ini
│   ├── tests/                    ← testes de API (pytest)
│   └── app/
│       ├── config.py             ← leitura das variáveis de ambiente
│       ├── db.py                 ← cliente Motor, MongoModel/BaseDocument (ObjectId→str, datas UTC), janela_dia()
│       ├── crud.py               ← helpers CRUD genéricos (listar/criar/obter/atualizar/deletar)
│       ├── dependencies.py       ← get_current_user (Bearer JWT | Bearer session | cookie session_token)
│       ├── routers/              ← um arquivo por recurso, todos sob /api
│       │   ├── auth.py           ← login, register, session (Google), logout, me
│       │   ├── agendamentos.py   ← CRUD + concluir (deduz insumos) + conflito de horário
│       │   ├── servicos.py       ← CRUD + insumos consumidos por serviço
│       │   ├── insumos.py        ← CRUD de estoque
│       │   ├── profissionais.py  ← CRUD da equipe
│       │   ├── estoque.py        ← alertas (mínimo + demanda prevista 7 dias)
│       │   ├── financeiro.py     ← resumo e lançamentos
│       │   ├── dashboard.py      ← faturamento por período
│       │   ├── debitos.py        ← débitos de clientes
│       │   ├── lembretes.py      ← lembretes + véspera (gerar/editar/enviar/enviar-todos/config)
│       │   └── ai.py             ← chat (SSE), gerar-mensagem (SSE), lembretes-vespera (SSE paralelo)
│       ├── schemas/              ← modelos Pydantic (request/response) por recurso
│       │   ├── usuario.py  agendamento.py  servico.py  insumo.py  profissional.py
│       │   ├── financeiro.py  estoque.py  debito.py  lembrete.py  ai.py
│       └── services/             ← regras de negócio e integrações
│           ├── auth.py           ← bcrypt + JWT
│           ├── ai.py             ← Claude Sonnet 4.5 (emergentintegrations), contexto do salão, prompts
│           ├── lembretes.py      ← agendamentos de amanhã, salvar mensagem, registrar envio
│           └── whatsapp.py       ← Twilio WhatsApp (REST/httpx), opcional
│
└── frontend/                     ← React 19 + CRACO (porta 3000)
    ├── package.json
    ├── .env                      ← REACT_APP_BACKEND_URL (veja .env.example)
    ├── .env.example
    ├── craco.config.js  jsconfig.json (alias "@/…" → src/)  tailwind.config.js  postcss.config.js
    ├── public/index.html
    └── src/
        ├── index.js  App.js      ← rotas (/, /app/agenda, /app/perfil, /app/atendimento, /app/estoque, /app/financeiro, /app/configuracoes)
        ├── index.css  App.css    ← design system ELO (variáveis, cards, chat, lembretes, insumos)
        ├── lib/api.js            ← axios (Bearer + cookies) e streamSSE() para respostas da IA
        ├── context/
        │   ├── AuthContext.jsx   ← login, register, loginWithGoogle, processSession, logout, updateProfile
        │   └── ToastContext.jsx  ← toasts (success / error / warning)
        ├── components/
        │   ├── AppShell.jsx      ← sidebar + topbar + <Outlet/>
        │   ├── AuthCallback.jsx  ← troca #session_id do Google por sessão
        │   ├── LembretesVespera.jsx  ← card "Lembretes de amanhã" (gerar com IA, editar, enviar)
        │   ├── ServicoInsumos.jsx    ← seção "Insumos consumidos" de cada serviço
        │   └── ui/               ← componentes shadcn/ui
        └── pages/
            ├── Landing.jsx       ← hero + modal login/cadastro + Google
            ├── Atendimento.jsx   ← WhatsApp rápido, conversas, chat Assistente ELO, lembretes de amanhã
            ├── Agenda.jsx  Estoque.jsx  Financeiro.jsx  Perfil.jsx  Configuracoes.jsx
```

## Rodando no VS Code (local)

Pré-requisitos: **Python 3.11+**, **Node 18+** com **Yarn**, **MongoDB** local (ou Atlas).

### 1. Backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate   |   macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
cp .env.example .env        # e edite os valores
uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

> O pacote `emergentintegrations` (IA) vem do índice extra acima — por isso o `--extra-index-url`.

Na primeira subida o backend cria índices e **dados demo** (admin, serviços, equipe, insumos, agendamentos de hoje/amanhã).

### 2. Frontend

```bash
cd frontend
yarn install
cp .env.example .env        # REACT_APP_BACKEND_URL=http://localhost:8001
yarn start                  # abre http://localhost:3000
```

### 3. Login

- **E-mail/senha**: `admin@elo.beauty` / `elo123456`
- **Google**: botão "Continuar com Google" (auth gerenciada pela Emergent — sem chaves)

### VS Code

A pasta `.vscode/` já traz:
- `launch.json` — **Backend: FastAPI (uvicorn)** e **Frontend: React** (F5 para depurar) e o composto **Full stack**
- `settings.json` — interpretador Python do `.venv`, formatação e exclusões
- `extensions.json` — Python, Pylance, ESLint, Prettier, Tailwind, MongoDB

## Variáveis de ambiente

### backend/.env

| Variável | Obrigatória | Descrição |
| --- | --- | --- |
| `MONGO_URL` | sim | ex.: `mongodb://localhost:27017` |
| `DB_NAME` | sim | ex.: `elo_beauty` |
| `SECRET_KEY` | sim | segredo do JWT |
| `EMERGENT_LLM_KEY` | sim | chave universal Emergent (IA Claude) |
| `CORS_ORIGINS` | não | `*` (padrão) ou lista separada por vírgula |
| `APP_TIMEZONE` | não | padrão `America/Sao_Paulo` (define "hoje/amanhã") |
| `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN` / `TWILIO_WHATSAPP_FROM` | não | ativam o envio automático de WhatsApp (ver `INTEGRACAO_WHATSAPP.md`) |

### frontend/.env

| Variável | Descrição |
| --- | --- |
| `REACT_APP_BACKEND_URL` | URL do backend **sem** `/api` (ex.: `http://localhost:8001`) |

## API (resumo)

Todas as rotas têm prefixo `/api` e exigem `Authorization: Bearer <token>` (exceto login/register/session/health).

| Recurso | Rotas |
| --- | --- |
| Auth | `POST /auth/login` · `POST /auth/register` · `POST /auth/session` · `POST /auth/logout` · `GET/PUT /auth/me` |
| Agenda | `GET/POST /agendamentos/` · `PUT/DELETE /agendamentos/{id}` · `PATCH /agendamentos/{id}/concluir` |
| Serviços | `GET/POST /servicos/` · `GET/PUT/DELETE /servicos/{id}` · `GET/POST /servicos/{id}/insumos` · `DELETE /servicos/{id}/insumos/{insumo_id}` |
| Estoque | `GET/POST /insumos/` · `GET/PUT/DELETE /insumos/{id}` · `GET /estoque/alertas` |
| Equipe | `GET/POST /profissionais/` · `GET/PUT/DELETE /profissionais/{id}` |
| Financeiro | `GET /financeiro/resumo` · `POST /financeiro/lancamentos` · `GET /dashboard/financeiro?data_inicio&data_fim` · `GET/POST/DELETE /debitos/` |
| Lembretes | `GET/POST /lembretes/` · `GET /lembretes/config` · `GET /lembretes/vespera` · `PUT /lembretes/vespera/{id}` · `POST /lembretes/vespera/{id}/enviar` · `POST /lembretes/vespera/enviar-todos` |
| IA | `POST /ai/chat` (SSE) · `GET /ai/chat/{session_id}/messages` · `POST /ai/gerar-mensagem` (SSE) · `POST /ai/lembretes-vespera` (SSE) |

Documentação interativa: `http://localhost:8001/docs`.

## Testes

```bash
cd backend && pytest -q
```

===== FILE: INTEGRACAO_WHATSAPP.md =====
# Integração WhatsApp — Lembretes de véspera (ELO Beauty Care)

Este guia descreve como funciona a **Confirmação automática** (lembretes de véspera gerados pela IA e enviados por WhatsApp) e como ativar o envio automático via **Twilio**.

## Como funciona

1. **Atendimento → card "Lembretes de amanhã"** lista todos os agendamentos de amanhã (status `confirmado`/`pendente`), no fuso `APP_TIMEZONE` (padrão `America/Sao_Paulo`).
2. **"Gerar todas com IA"** chama `POST /api/ai/lembretes-vespera` — o Claude Sonnet 4.5 escreve uma mensagem curta e personalizada (nome da cliente, serviço, horário, profissional) para cada agendamento. O progresso chega por SSE e cada linha é preenchida conforme fica pronta. As mensagens ficam salvas no agendamento (`agendamentos.lembrete.mensagem`) e podem ser editadas na própria linha.
3. **Envio** — duas opções por cliente:
   - **WhatsApp (wa.me)**: abre o WhatsApp Web/celular com a mensagem pronta (um clique por cliente, sem custo, sem chaves). Ao clicar, o lembrete é marcado como enviado (`canal = whatsapp_link`).
   - **Enviar (Twilio)**: envio automático pela API do Twilio. Também existe **"Enviar todas"** que dispara em lote todas as mensagens prontas e ainda não enviadas.
4. Todo envio é registrado também na coleção `lembretes` (histórico exibido em "Lembretes registrados").

## Ativando o envio automático (Twilio)

1. Crie/acesse a conta em https://console.twilio.com
2. Copie **Account SID** (`AC…`) e **Auth Token** (Dashboard → Account Info).
3. Para testar sem aprovação da Meta, use o **WhatsApp Sandbox**: *Messaging → Try it out → Send a WhatsApp message*. O remetente é `whatsapp:+14155238886` e cada celular que receberá mensagens precisa antes enviar `join <código-do-sandbox>` para esse número.
   Em produção, troque pelo seu número WhatsApp Business aprovado (`whatsapp:+55DDDNUMERO`).
4. Preencha no `backend/.env`:

```
TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
TWILIO_AUTH_TOKEN="seu_auth_token"
TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"
APP_TIMEZONE="America/Sao_Paulo"
```

5. Reinicie o backend. O card passa a mostrar os botões **Enviar** / **Enviar todas** habilitados (`GET /api/lembretes/config` → `twilio_configurado: true`).

Sem credenciais, tudo continua funcionando com os links wa.me — apenas o envio automático fica desativado (aviso amarelo no card).

## Arquivos envolvidos

| Camada | Arquivo | Papel |
| --- | --- | --- |
| Backend | `backend/app/services/whatsapp.py` | Módulo isolado do Twilio (REST via `httpx`): `configurado()`, `normalizar_telefone()` (E.164 +55), `link_wa()`, `enviar()` |
| Backend | `backend/app/services/lembretes.py` | Agendamentos de amanhã, salvar mensagem, registrar envio/erro |
| Backend | `backend/app/routers/lembretes.py` | Endpoints `/api/lembretes/vespera*` e `/api/lembretes/config` |
| Backend | `backend/app/routers/ai.py` → `gerar_lembretes_vespera` | Geração paralela (3 simultâneas) com progresso SSE |
| Backend | `backend/app/services/ai.py` → `prompt_mensagem_whatsapp(..., vespera=True)` | Prompt da mensagem |
| Backend | `backend/app/schemas/lembrete.py` | Modelos Pydantic |
| Backend | `backend/app/config.py` | Leitura das variáveis `TWILIO_*` e `APP_TIMEZONE` |
| Frontend | `frontend/src/components/LembretesVespera.jsx` | Card completo (lista, gerar, editar, enviar) |
| Frontend | `frontend/src/lib/api.js` → `streamSSE()` | Leitura do stream de progresso |

## Endpoints

| Método | Rota | Descrição |
| --- | --- | --- |
| GET | `/api/lembretes/config` | `{ twilio_configurado, sandbox, remetente }` |
| GET | `/api/lembretes/vespera` | Agendamentos de amanhã com `lembrete` (mensagem, gerado_em, enviado_em, canal, twilio_sid, erro) |
| POST | `/api/ai/lembretes-vespera` | Body `{ agendamento_ids?: string[], tom?: string }` — SSE: `{total}`, `{agendamento_id, mensagem}`…, `{done}` |
| PUT | `/api/lembretes/vespera/{agendamento_id}` | Body `{ mensagem }` — edita a mensagem |
| POST | `/api/lembretes/vespera/{agendamento_id}/enviar` | Body `{ canal: "twilio" \| "whatsapp_link", mensagem? }` → `{ ok, detalhe, item }` |
| POST | `/api/lembretes/vespera/enviar-todos` | Envia via Twilio todas as prontas e não enviadas → `EnvioResultado[]` (503 se Twilio não configurado) |

## Formato de telefone

`normalizar_telefone()` aceita `55 42 99999-0000`, `(42) 99999-0000`, `5542999990000` e devolve `+5542999990000`. Números com 10–11 dígitos (DDD + número) recebem o DDI `55` automaticamente. O Twilio recebe `whatsapp:+55…`.

## Teste rápido (curl)

```bash
API=https://SEU-BACKEND
TOKEN=$(curl -s -X POST $API/api/auth/login -H "Content-Type: application/json" -d '{"email":"admin@elo.beauty","senha":"elo123456"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
curl -s $API/api/lembretes/config -H "Authorization: Bearer $TOKEN"
curl -s $API/api/lembretes/vespera -H "Authorization: Bearer $TOKEN"
curl -s -N -X POST $API/api/ai/lembretes-vespera -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{}'
```

===== FILE: auth_testing.md =====
# Auth-Gated App Testing Playbook (Emergent Google Auth)

Este app usa autenticação híbrida:
- **JWT** (e-mail/senha): `POST /api/auth/login` → `access_token` (Bearer). Admin: `admin@elo.beauty` / `elo123456`.
- **Google (Emergent-managed)**: frontend redireciona para `https://auth.emergentagent.com/?redirect=<origin>/app/atendimento`; volta com `#session_id=...`; frontend chama `POST /api/auth/session` → backend troca no Emergent, cria doc em `user_sessions`, seta cookie httpOnly `session_token` e devolve `access_token` (o próprio session_token) + `user`.
- `get_current_user` aceita `Authorization: Bearer <jwt|session_token>` ou cookie `session_token`.

## Step 1: Criar usuário + sessão de teste (simula login Google)
```bash
mongosh --quiet --eval "
use('test_database');
var sessionToken = 'test_session_' + Date.now();
var u = db.usuarios.findOneAndUpdate(
  {email: 'google.tester@example.com'},
  {\$setOnInsert: {email: 'google.tester@example.com', nome: 'Google Tester', business: 'Studio Teste', city: null, picture: 'https://via.placeholder.com/150', criado_em: new Date()}},
  {upsert: true, returnDocument: 'after'}
);
db.user_sessions.insertOne({user_id: u._id.toString(), session_token: sessionToken, expires_at: new Date(Date.now() + 7*24*60*60*1000), created_at: new Date()});
print('Session token: ' + sessionToken);
"
```

## Step 2: Testar backend com o session_token
```bash
API=$(grep REACT_APP_BACKEND_URL /app/frontend/.env | cut -d '=' -f2)
curl -s "$API/api/auth/me" -H "Authorization: Bearer $SESSION_TOKEN"
curl -s "$API/api/agendamentos/" -H "Authorization: Bearer $SESSION_TOKEN"
# via cookie:
curl -s "$API/api/auth/me" -H "Cookie: session_token=$SESSION_TOKEN"
```

## Step 3: Browser
```python
await page.context.add_cookies([{
    "name": "session_token", "value": SESSION_TOKEN,
    "domain": "<host do preview>", "path": "/", "httpOnly": True, "secure": True, "sameSite": "None"
}])
# O frontend também aceita o token em localStorage:
await page.goto(APP_URL)
await page.evaluate(f"localStorage.setItem('elo_token', '{SESSION_TOKEN}')")
await page.goto(APP_URL + "/app/atendimento")
```

## Limpeza
```bash
mongosh --quiet --eval "use('test_database'); db.usuarios.deleteMany({email: /google\.tester|test\.user/}); db.user_sessions.deleteMany({session_token: /test_session/});"
```

## Checklist
- [ ] `/api/auth/me` devolve o usuário com `id` (string), sem `_id`
- [ ] Sessão expirada → 401
- [ ] Logout (`POST /api/auth/logout`) remove a sessão e o cookie
- [ ] Páginas /app/* carregam sem redirecionar para "/"
- [ ] Detecção do callback usa `useLocation().hash` (App.js → AppRouter)

===== FILE: .gitignore =====
# See https://help.github.com/articles/ignoring-files/ for more about ignoring files.

# IDE and editors
.idea/

# Dependencies
node_modules/
/node_modules
/.pnp
.pnp.js
.yarn/install-state.gz
.yarn/*
!.yarn/patches
!.yarn/plugins
!.yarn/releases
!.yarn/versions

# Testing
/coverage

# Next.js
/.next/
/out/
next-env.d.ts
*.tsbuildinfo

# Production builds
/build
dist/
dist

# Environment files (comprehensive coverage)

*token.json*
*credentials.json*

# Logs and debug files
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.pnpm-debug.log*
dump.rdb

# System files
.DS_Store
*.pem

# Python
__pycache__/
*pyc*
venv/
.venv/

# Development tools
chainlit.md
.chainlit
.ipynb_checkpoints/
.ac

# Deployment
.vercel

# Data and databases
agenthub/agents/youtube/db

# Archive files and large assets
**/*.zip
**/*.tar.gz
**/*.tar
**/*.tgz
*.pack
*.deb
*.dylib

# Build caches
.cache/

memory/test_credentials.md

# Mobile development
android-sdk/

# overlay black-box crash/user-report dumps — session data, never history
**/.emergent/recordings/

===== FILE: backend/.env.example =====
MONGO_URL="mongodb://localhost:27017"
DB_NAME="elo_beauty"
CORS_ORIGINS="*"
SECRET_KEY="troque-por-um-segredo-longo-e-aleatorio"
EMERGENT_LLM_KEY="sk-emergent-sua-chave"
APP_TIMEZONE="America/Sao_Paulo"
TWILIO_ACCOUNT_SID=""
TWILIO_AUTH_TOKEN=""
TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"

===== FILE: backend/app/__init__.py =====

===== FILE: backend/app/config.py =====
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

MONGO_URL = os.environ["MONGO_URL"]
DB_NAME = os.environ["DB_NAME"]
SECRET_KEY = os.environ["SECRET_KEY"]
EMERGENT_LLM_KEY = os.environ["EMERGENT_LLM_KEY"]
CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")
TIMEZONE = os.environ.get("APP_TIMEZONE", "America/Sao_Paulo")

TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
TWILIO_WHATSAPP_FROM = os.environ.get("TWILIO_WHATSAPP_FROM", "").strip()

JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
SESSION_DAYS = 7
EMERGENT_AUTH_SESSION_URL = "https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data"

===== FILE: backend/app/crud.py =====
from fastapi import HTTPException
from pydantic import BaseModel
from pymongo import ReturnDocument

from app.db import oid


async def listar(col, model, ordem: int = 1) -> list:
    return [model.from_mongo(d) async for d in col.find().sort("_id", ordem)]


async def criar(col, model, body: BaseModel, extra: dict | None = None):
    doc = {**body.model_dump(), **(extra or {})}
    res = await col.insert_one(doc)
    return model.from_mongo({**doc, "_id": res.inserted_id})


async def obter(col, model, item_id: str, nao_encontrado: str):
    doc = await col.find_one({"_id": oid(item_id, nao_encontrado)})
    if doc is None:
        raise HTTPException(status_code=404, detail=nao_encontrado)
    return model.from_mongo(doc)


async def atualizar(col, model, item_id: str, body: BaseModel, nao_encontrado: str):
    campos = body.model_dump(exclude_unset=True, exclude_none=True)
    if not campos:
        return await obter(col, model, item_id, nao_encontrado)
    doc = await col.find_one_and_update(
        {"_id": oid(item_id, nao_encontrado)}, {"$set": campos}, return_document=ReturnDocument.AFTER
    )
    if doc is None:
        raise HTTPException(status_code=404, detail=nao_encontrado)
    return model.from_mongo(doc)


async def deletar(col, item_id: str, nao_encontrado: str) -> None:
    res = await col.delete_one({"_id": oid(item_id, nao_encontrado)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail=nao_encontrado)

===== FILE: backend/app/db.py =====
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Optional
from zoneinfo import ZoneInfo

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import AliasChoices, BaseModel, BeforeValidator, ConfigDict, Field, field_validator

from app import config

client = AsyncIOMotorClient(config.MONGO_URL)
db = client[config.DB_NAME]


def _to_str(v: Any) -> Any:
    return str(v) if isinstance(v, ObjectId) else v


PyObjectId = Annotated[str, BeforeValidator(_to_str)]


def utc(dt: datetime) -> datetime:
    return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt


def now() -> datetime:
    return datetime.now(timezone.utc)


TZ = ZoneInfo(config.TIMEZONE)


def local(dt: datetime) -> datetime:
    return utc(dt).astimezone(TZ)


def janela_dia(offset_dias: int = 0) -> tuple[datetime, datetime]:
    inicio = now().astimezone(TZ).replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=offset_dias)
    return inicio, inicio + timedelta(days=1)


def oid(value: str, detail: str = "Registro não encontrado") -> ObjectId:
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(status_code=404, detail=detail)


class MongoModel(BaseModel):
    """Normaliza ObjectId → str e datetimes naive (UTC) → aware em qualquer nível."""

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("*", mode="before")
    @classmethod
    def _normalizar(cls, v: Any) -> Any:
        if isinstance(v, datetime):
            return utc(v)
        return _to_str(v)


class BaseDocument(MongoModel):
    id: Optional[PyObjectId] = Field(default=None, validation_alias=AliasChoices("_id", "id"))

    def to_mongo(self) -> dict:
        return self.model_dump(exclude={"id"}, exclude_none=True)

    @classmethod
    def from_mongo(cls, doc: dict | None):
        return cls.model_validate(doc) if doc is not None else None

===== FILE: backend/app/dependencies.py =====
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

===== FILE: backend/app/routers/__init__.py =====

===== FILE: backend/app/routers/agendamentos.py =====
from datetime import datetime, timedelta

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from pymongo import ReturnDocument

from app.db import db, oid
from app.dependencies import get_current_user
from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse, AgendamentoUpdate

router = APIRouter(prefix="/agendamentos", tags=["agendamentos"], dependencies=[Depends(get_current_user)])
NAO_ENCONTRADO = "Agendamento não encontrado"


async def _mapa(col, ids: list[ObjectId]) -> dict:
    return {d["_id"]: d for d in await col.find({"_id": {"$in": ids}}).to_list(len(ids) or 1)} if ids else {}


async def _responses(docs: list[dict], alertas: list[str] | None = None) -> list[AgendamentoResponse]:
    servicos = await _mapa(db.servicos, [d["servico_id"] for d in docs])
    clientes = await _mapa(db.clientes, [d["cliente_id"] for d in docs])
    profs = await _mapa(db.profissionais, [d["profissional_id"] for d in docs])
    out = []
    for d in docs:
        srv = servicos.get(d["servico_id"], {})
        out.append(
            AgendamentoResponse.from_mongo(
                {
                    **d,
                    "servico_nome": srv.get("nome", "—"),
                    "servico_valor": srv.get("valor", 0.0),
                    "cliente_nome": clientes.get(d["cliente_id"], {}).get("nome"),
                    "profissional_nome": profs.get(d["profissional_id"], {}).get("nome", "—"),
                    "alertas_estoque": alertas or [],
                }
            )
        )
    return out


async def _obter_doc(agendamento_id: str) -> dict:
    doc = await db.agendamentos.find_one({"_id": oid(agendamento_id, NAO_ENCONTRADO)})
    if doc is None:
        raise HTTPException(status_code=404, detail=NAO_ENCONTRADO)
    return doc


async def _exigir(col, item_id: str, detail: str) -> dict:
    doc = await col.find_one({"_id": oid(item_id, detail)})
    if doc is None:
        raise HTTPException(status_code=404, detail=detail)
    return doc


async def _resolver_cliente(body: AgendamentoCreate) -> dict:
    if body.cliente_id:
        return await _exigir(db.clientes, body.cliente_id, "Cliente não encontrado")
    telefone = body.cliente_telefone.strip()
    cliente = await db.clientes.find_one({"telefone": telefone})
    if cliente:
        if body.cliente_nome and not cliente.get("nome"):
            await db.clientes.update_one({"_id": cliente["_id"]}, {"$set": {"nome": body.cliente_nome}})
        return cliente
    novo = {"telefone": telefone, "nome": body.cliente_nome}
    res = await db.clientes.insert_one(novo)
    return {**novo, "_id": res.inserted_id}


async def _checar_conflito(profissional_id: ObjectId, inicio: datetime, fim: datetime, ignorar: ObjectId | None = None):
    filtro = {"profissional_id": profissional_id, "data_hora_inicio": {"$lt": fim}, "data_hora_fim": {"$gt": inicio}}
    if ignorar is not None:
        filtro["_id"] = {"$ne": ignorar}
    if await db.agendamentos.find_one(filtro):
        raise HTTPException(status_code=409, detail="Já existe um agendamento neste horário")


@router.get("/", response_model=list[AgendamentoResponse])
async def listar(
    profissional_id: str | None = Query(None),
    data_inicio: str | None = Query(None),
    data_fim: str | None = Query(None),
):
    filtro: dict = {}
    if profissional_id:
        filtro["profissional_id"] = oid(profissional_id, "Profissional não encontrado")
    periodo = {}
    if data_inicio:
        periodo["$gte"] = datetime.fromisoformat(data_inicio)
    if data_fim:
        periodo["$lt"] = datetime.fromisoformat(data_fim)
    if periodo:
        filtro["data_hora_inicio"] = periodo
    docs = await db.agendamentos.find(filtro).sort("data_hora_inicio", 1).to_list(500)
    return await _responses(docs)


@router.post("/", response_model=AgendamentoResponse, status_code=201)
async def criar(body: AgendamentoCreate):
    servico = await _exigir(db.servicos, body.servico_id, "Serviço não encontrado")
    profissional = await _exigir(db.profissionais, body.profissional_id, "Profissional não encontrado")
    cliente = await _resolver_cliente(body)

    inicio = body.data_hora_inicio
    fim = body.data_hora_fim or (inicio + timedelta(minutes=servico["duracao_minutos"]))
    await _checar_conflito(profissional["_id"], inicio, fim)

    doc = {
        "cliente_id": cliente["_id"],
        "profissional_id": profissional["_id"],
        "servico_id": servico["_id"],
        "data_hora_inicio": inicio,
        "data_hora_fim": fim,
        "status": "confirmado",
        "salao_id": 1,
    }
    res = await db.agendamentos.insert_one(doc)
    return (await _responses([{**doc, "_id": res.inserted_id}]))[0]


async def _deduzir_insumos(servico_id: ObjectId) -> list[str]:
    relacoes = await db.servico_insumos.find({"servico_id": servico_id}).to_list(100)
    alertas: list[str] = []
    for rel in relacoes:
        insumo = await db.insumos.find_one({"_id": rel["insumo_id"]})
        if insumo is None:
            continue
        nova_qtd = insumo["quantidade_atual"] - rel["quantidade_utilizada"]
        if nova_qtd < 0:
            raise HTTPException(
                status_code=409,
                detail=f"Estoque insuficiente para '{insumo['nome']}': tem {insumo['quantidade_atual']}, precisa de {rel['quantidade_utilizada']}",
            )
        await db.insumos.update_one({"_id": insumo["_id"]}, {"$set": {"quantidade_atual": nova_qtd}})
        if nova_qtd <= insumo["quantidade_minima_alerta"]:
            alertas.append(f"{insumo['nome']} está com estoque baixo ({nova_qtd} un)")
    return alertas


@router.patch("/{agendamento_id}/concluir", response_model=AgendamentoResponse)
async def concluir(agendamento_id: str):
    doc = await _obter_doc(agendamento_id)
    alertas = await _deduzir_insumos(doc["servico_id"]) if doc["status"] != "concluido" else []
    doc = await db.agendamentos.find_one_and_update(
        {"_id": doc["_id"]}, {"$set": {"status": "concluido"}}, return_document=ReturnDocument.AFTER
    )
    return (await _responses([doc], alertas))[0]


@router.put("/{agendamento_id}", response_model=AgendamentoResponse)
async def atualizar(agendamento_id: str, body: AgendamentoUpdate):
    atual = await _obter_doc(agendamento_id)
    campos: dict = {}
    if body.servico_id is not None:
        campos["servico_id"] = (await _exigir(db.servicos, body.servico_id, "Serviço não encontrado"))["_id"]
    if body.profissional_id is not None:
        campos["profissional_id"] = (await _exigir(db.profissionais, body.profissional_id, "Profissional não encontrado"))["_id"]
    if body.cliente_id is not None:
        campos["cliente_id"] = (await _exigir(db.clientes, body.cliente_id, "Cliente não encontrado"))["_id"]
    for campo in ("data_hora_inicio", "data_hora_fim", "status"):
        valor = getattr(body, campo)
        if valor is not None:
            campos[campo] = valor

    if "data_hora_inicio" in campos or "data_hora_fim" in campos or "profissional_id" in campos:
        await _checar_conflito(
            campos.get("profissional_id", atual["profissional_id"]),
            campos.get("data_hora_inicio", atual["data_hora_inicio"]),
            campos.get("data_hora_fim", atual["data_hora_fim"]),
            ignorar=atual["_id"],
        )

    if campos:
        atual = await db.agendamentos.find_one_and_update(
            {"_id": atual["_id"]}, {"$set": campos}, return_document=ReturnDocument.AFTER
        )
    return (await _responses([atual]))[0]


@router.delete("/{agendamento_id}", status_code=204)
async def deletar(agendamento_id: str):
    res = await db.agendamentos.delete_one({"_id": oid(agendamento_id, NAO_ENCONTRADO)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail=NAO_ENCONTRADO)

===== FILE: backend/app/routers/ai.py =====
import asyncio
import json
import logging
from uuid import uuid4

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.db import db, local, now
from app.dependencies import get_current_user
from app.schemas.ai import ChatMessage, ChatRequest, GerarMensagemRequest
from app.schemas.lembrete import LembretesVesperaIARequest
from app.schemas.usuario import UsuarioResponse
from app.services import ai
from app.services import lembretes as lembretes_service

router = APIRouter(prefix="/ai", tags=["ai"])
logger = logging.getLogger("elo.ai")

SSE_HEADERS = {"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
CONCORRENCIA_IA = 3


def _sse(payload: dict) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"


async def _stream(chat, texto: str, meta: dict, ao_final=None):
    yield _sse(meta)
    partes: list[str] = []
    try:
        async for delta in ai.stream_texto(chat, texto):
            partes.append(delta)
            yield _sse({"delta": delta})
    except Exception:  # noqa: BLE001
        logger.exception("Falha na IA")
        yield _sse({"error": "O assistente não conseguiu responder agora. Tente novamente."})
    if partes and ao_final:
        await ao_final("".join(partes))
    yield _sse({"done": True})


@router.get("/chat/{session_id}/messages", response_model=list[ChatMessage])
async def historico(session_id: str, user: UsuarioResponse = Depends(get_current_user)):
    docs = await db.chat_messages.find({"session_id": session_id, "user_id": user.id}).sort("criado_em", 1).to_list(200)
    return [ChatMessage.from_mongo(d) for d in docs]


@router.post("/chat")
async def chat(body: ChatRequest, user: UsuarioResponse = Depends(get_current_user)):
    session_id = body.session_id or uuid4().hex
    historico_docs = await db.chat_messages.find({"session_id": session_id, "user_id": user.id}).sort("criado_em", 1).to_list(60)
    historico = [{"role": m["role"], "content": m["content"]} for m in historico_docs]

    system = await ai.contexto_salao(user)
    llm = ai.novo_chat(session_id, system, historico)

    await db.chat_messages.insert_one(
        {"session_id": session_id, "user_id": user.id, "role": "user", "content": body.message, "criado_em": now()}
    )

    async def salvar_resposta(texto: str):
        await db.chat_messages.insert_one(
            {"session_id": session_id, "user_id": user.id, "role": "assistant", "content": texto, "criado_em": now()}
        )

    return StreamingResponse(
        _stream(llm, body.message, {"session_id": session_id}, salvar_resposta),
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


@router.post("/gerar-mensagem")
async def gerar_mensagem(body: GerarMensagemRequest, user: UsuarioResponse = Depends(get_current_user)):
    system, pedido = ai.prompt_mensagem_whatsapp(
        user, body.tom, cliente_nome=body.cliente_nome, servico=body.servico, horario=body.horario
    )
    llm = ai.novo_chat(f"msg-{uuid4().hex}", system)
    return StreamingResponse(_stream(llm, pedido, {"tipo": "mensagem"}), media_type="text/event-stream", headers=SSE_HEADERS)


@router.post("/lembretes-vespera")
async def gerar_lembretes_vespera(body: LembretesVesperaIARequest, user: UsuarioResponse = Depends(get_current_user)):
    """Gera (em paralelo, com streaming de progresso) uma mensagem personalizada por agendamento de amanhã."""
    itens = await lembretes_service.listar_amanha(body.agendamento_ids)
    semaforo = asyncio.Semaphore(CONCORRENCIA_IA)

    async def gerar(item):
        async with semaforo:
            system, pedido = ai.prompt_mensagem_whatsapp(
                user,
                body.tom,
                cliente_nome=item.cliente_nome,
                servico=item.servico_nome,
                horario=f"amanhã às {local(item.data_hora_inicio).strftime('%H:%M')}",
                profissional=item.profissional_nome,
                vespera=True,
            )
            texto = await ai.gerar_texto(f"vespera-{item.id}-{uuid4().hex[:6]}", system, pedido)
            await lembretes_service.salvar_mensagem(item.id, texto)
            return item.id, texto

    async def progresso():
        yield _sse({"total": len(itens)})
        tarefas = {asyncio.ensure_future(gerar(i)): i.id for i in itens}
        for fut in asyncio.as_completed(tarefas):
            try:
                agendamento_id, texto = await fut
                yield _sse({"agendamento_id": agendamento_id, "mensagem": texto})
            except Exception:  # noqa: BLE001
                logger.exception("Falha ao gerar lembrete de véspera")
                yield _sse({"falha": "Não foi possível gerar uma das mensagens."})
        yield _sse({"done": True})

    return StreamingResponse(progresso(), media_type="text/event-stream", headers=SSE_HEADERS)

===== FILE: backend/app/routers/auth.py =====
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

===== FILE: backend/app/routers/dashboard.py =====
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query

from app.db import db
from app.dependencies import get_current_user
from app.schemas.financeiro import FaturamentoResponse

router = APIRouter(prefix="/dashboard", tags=["dashboard"], dependencies=[Depends(get_current_user)])


@router.get("/financeiro", response_model=FaturamentoResponse)
async def financeiro(data_inicio: str = Query(...), data_fim: str = Query(...)):
    dt_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    dt_fim = datetime.strptime(data_fim, "%Y-%m-%d").replace(tzinfo=timezone.utc) + timedelta(days=1)

    concluidos = await db.agendamentos.find(
        {"status": "concluido", "data_hora_inicio": {"$gte": dt_inicio, "$lt": dt_fim}}
    ).to_list(5000)
    ids = list({a["servico_id"] for a in concluidos})
    valores = {s["_id"]: s["valor"] for s in await db.servicos.find({"_id": {"$in": ids}}).to_list(len(ids) or 1)} if ids else {}
    total = sum(valores.get(a["servico_id"], 0.0) for a in concluidos)
    return FaturamentoResponse(total=total, data_inicio=data_inicio, data_fim=data_fim)

===== FILE: backend/app/routers/debitos.py =====
from fastapi import APIRouter, Depends

from app import crud
from app.db import db
from app.dependencies import get_current_user
from app.schemas.debito import DebitoCreate, DebitoResponse

router = APIRouter(prefix="/debitos", tags=["debitos"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[DebitoResponse])
async def listar():
    return await crud.listar(db.debitos, DebitoResponse, ordem=-1)


@router.post("/", response_model=DebitoResponse, status_code=201)
async def criar(body: DebitoCreate):
    return await crud.criar(db.debitos, DebitoResponse, body, {"salao_id": 1})


@router.delete("/{debito_id}", status_code=204)
async def deletar(debito_id: str):
    await crud.deletar(db.debitos, debito_id, "Débito não encontrado")

===== FILE: backend/app/routers/estoque.py =====
from datetime import timedelta

from fastapi import APIRouter, Depends

from app.db import db, now
from app.dependencies import get_current_user
from app.schemas.estoque import AlertaEstoqueResponse

router = APIRouter(prefix="/estoque", tags=["estoque"], dependencies=[Depends(get_current_user)])


async def _demanda_proximos_dias(dias: int = 7) -> dict:
    agora = now()
    pipeline = [
        {"$match": {"status": "confirmado", "data_hora_inicio": {"$gte": agora, "$lt": agora + timedelta(days=dias)}}},
        {"$group": {"_id": "$servico_id", "total": {"$sum": 1}}},
    ]
    counts = {r["_id"]: r["total"] async for r in db.agendamentos.aggregate(pipeline)}
    if not counts:
        return {}
    demanda: dict = {}
    async for rel in db.servico_insumos.find({"servico_id": {"$in": list(counts)}}):
        demanda[rel["insumo_id"]] = demanda.get(rel["insumo_id"], 0) + rel["quantidade_utilizada"] * counts[rel["servico_id"]]
    return demanda


@router.get("/alertas", response_model=list[AlertaEstoqueResponse])
async def alertas_estoque():
    demanda = await _demanda_proximos_dias()
    insumos = {i["_id"]: i for i in await db.insumos.find().to_list(500)}
    alertas: list[AlertaEstoqueResponse] = []

    for insumo_id, necessario in demanda.items():
        insumo = insumos.get(insumo_id)
        if insumo and insumo["quantidade_atual"] < necessario:
            alertas.append(
                AlertaEstoqueResponse(
                    insumo_id=str(insumo_id),
                    nome=insumo["nome"],
                    quantidade_atual=insumo["quantidade_atual"],
                    quantidade_minima_alerta=insumo["quantidade_minima_alerta"],
                    demanda_prevista=round(necessario, 1),
                    tipo="demanda",
                    mensagem=f"Reposição necessária: {insumo['nome']} (tem {insumo['quantidade_atual']}, precisa de {necessario:.0f})",
                )
            )

    com_alerta = {a.insumo_id for a in alertas}
    for insumo in insumos.values():
        if str(insumo["_id"]) in com_alerta or insumo["quantidade_atual"] > insumo["quantidade_minima_alerta"]:
            continue
        alertas.append(
            AlertaEstoqueResponse(
                insumo_id=str(insumo["_id"]),
                nome=insumo["nome"],
                quantidade_atual=insumo["quantidade_atual"],
                quantidade_minima_alerta=insumo["quantidade_minima_alerta"],
                demanda_prevista=0,
                tipo="minimo",
                mensagem=f"Estoque baixo: {insumo['nome']} ({insumo['quantidade_atual']}/{insumo['quantidade_minima_alerta']} mín.)",
            )
        )
    return alertas

===== FILE: backend/app/routers/financeiro.py =====
from fastapi import APIRouter, Depends

from app import crud
from app.db import db, now
from app.dependencies import get_current_user
from app.schemas.financeiro import MovimentoCreate, MovimentoResponse, ResumoFinanceiroResponse

router = APIRouter(prefix="/financeiro", tags=["financeiro"], dependencies=[Depends(get_current_user)])


@router.get("/resumo", response_model=ResumoFinanceiroResponse)
async def resumo():
    docs = await db.movimentos_financeiros.find().sort("data", -1).to_list(1000)
    entradas = sum(m["valor"] for m in docs if m["tipo"] == "entrada")
    saidas = sum(m["valor"] for m in docs if m["tipo"] == "saida")
    return ResumoFinanceiroResponse(
        entradas=entradas,
        saidas=saidas,
        saldo=entradas - saidas,
        lancamentos=[MovimentoResponse.from_mongo(m) for m in docs],
    )


@router.post("/lancamentos", response_model=MovimentoResponse, status_code=201)
async def criar_lancamento(body: MovimentoCreate):
    return await crud.criar(db.movimentos_financeiros, MovimentoResponse, body, {"data": now(), "salao_id": 1})

===== FILE: backend/app/routers/insumos.py =====
from fastapi import APIRouter, Depends

from app import crud
from app.db import db, oid
from app.dependencies import get_current_user
from app.schemas.insumo import InsumoCreate, InsumoResponse, InsumoUpdate

router = APIRouter(prefix="/insumos", tags=["insumos"], dependencies=[Depends(get_current_user)])
NAO_ENCONTRADO = "Insumo não encontrado"


@router.get("/", response_model=list[InsumoResponse])
async def listar():
    return await crud.listar(db.insumos, InsumoResponse)


@router.post("/", response_model=InsumoResponse, status_code=201)
async def criar(body: InsumoCreate):
    return await crud.criar(db.insumos, InsumoResponse, body, {"salao_id": 1})


@router.get("/{insumo_id}", response_model=InsumoResponse)
async def obter(insumo_id: str):
    return await crud.obter(db.insumos, InsumoResponse, insumo_id, NAO_ENCONTRADO)


@router.put("/{insumo_id}", response_model=InsumoResponse)
async def atualizar(insumo_id: str, body: InsumoUpdate):
    return await crud.atualizar(db.insumos, InsumoResponse, insumo_id, body, NAO_ENCONTRADO)


@router.delete("/{insumo_id}", status_code=204)
async def deletar(insumo_id: str):
    await crud.deletar(db.insumos, insumo_id, NAO_ENCONTRADO)
    await db.servico_insumos.delete_many({"insumo_id": oid(insumo_id)})

===== FILE: backend/app/routers/lembretes.py =====
from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.db import db, now
from app.dependencies import get_current_user
from app.schemas.lembrete import (
    EnviarLembreteRequest,
    EnvioResultado,
    LembreteCreate,
    LembreteMensagemUpdate,
    LembreteResponse,
    LembreteVesperaResponse,
    WhatsAppConfigResponse,
)
from app.services import lembretes as svc
from app.services import whatsapp

router = APIRouter(prefix="/lembretes", tags=["lembretes"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[LembreteResponse])
async def listar():
    return await crud.listar(db.lembretes, LembreteResponse, ordem=-1)


@router.post("/", response_model=LembreteResponse, status_code=201)
async def criar(body: LembreteCreate):
    return await crud.criar(db.lembretes, LembreteResponse, body, {"criado_em": now(), "salao_id": 1})


# ---------- Lembretes de véspera ----------


@router.get("/config", response_model=WhatsAppConfigResponse)
async def config_whatsapp():
    return WhatsAppConfigResponse(
        twilio_configurado=whatsapp.configurado(),
        sandbox=whatsapp.usando_sandbox(),
        remetente=whatsapp.remetente_mascarado(),
    )


@router.get("/vespera", response_model=list[LembreteVesperaResponse])
async def listar_vespera():
    return await svc.listar_amanha()


@router.put("/vespera/{agendamento_id}", response_model=LembreteVesperaResponse)
async def editar_mensagem(agendamento_id: str, body: LembreteMensagemUpdate):
    return await svc.salvar_mensagem(agendamento_id, body.mensagem)


async def _enviar(item: LembreteVesperaResponse, canal: str, mensagem: str | None) -> EnvioResultado:
    texto = (mensagem or item.lembrete.mensagem or "").strip()
    if not texto:
        return EnvioResultado(agendamento_id=item.id, ok=False, detalhe="Gere ou escreva a mensagem antes de enviar", item=item)
    if texto != item.lembrete.mensagem:
        item = await svc.salvar_mensagem(item.id, texto)

    if canal == "twilio":
        if not item.telefone_e164:
            return EnvioResultado(agendamento_id=item.id, ok=False, detalhe="Telefone da cliente inválido", item=item)
        try:
            sid = await whatsapp.enviar(item.telefone_e164, texto)
        except whatsapp.EnvioWhatsAppError as exc:
            item = await svc.registrar_erro(item, str(exc))
            return EnvioResultado(agendamento_id=item.id, ok=False, detalhe=str(exc), item=item)
        item = await svc.registrar_envio(item, "twilio", texto, sid)
    else:
        item = await svc.registrar_envio(item, "whatsapp_link", texto)
    return EnvioResultado(agendamento_id=item.id, ok=True, item=item)


@router.post("/vespera/enviar-todos", response_model=list[EnvioResultado])
async def enviar_todos():
    if not whatsapp.configurado():
        raise HTTPException(status_code=503, detail="Envio automático desativado: configure TWILIO_* no backend/.env")
    pendentes = [i for i in await svc.listar_amanha() if i.lembrete.mensagem and not i.lembrete.enviado_em]
    return [await _enviar(i, "twilio", None) for i in pendentes]


@router.post("/vespera/{agendamento_id}/enviar", response_model=EnvioResultado)
async def enviar_um(agendamento_id: str, body: EnviarLembreteRequest):
    item = await svc.obter(agendamento_id)
    if body.canal == "twilio" and not whatsapp.configurado():
        raise HTTPException(status_code=503, detail="Envio automático desativado: configure TWILIO_* no backend/.env")
    return await _enviar(item, body.canal, body.mensagem)

===== FILE: backend/app/routers/profissionais.py =====
from fastapi import APIRouter, Depends

from app import crud
from app.db import db
from app.dependencies import get_current_user
from app.schemas.profissional import ProfissionalCreate, ProfissionalResponse, ProfissionalUpdate

router = APIRouter(prefix="/profissionais", tags=["profissionais"], dependencies=[Depends(get_current_user)])
NAO_ENCONTRADO = "Profissional não encontrado"


@router.get("/", response_model=list[ProfissionalResponse])
async def listar():
    return await crud.listar(db.profissionais, ProfissionalResponse)


@router.post("/", response_model=ProfissionalResponse, status_code=201)
async def criar(body: ProfissionalCreate):
    return await crud.criar(db.profissionais, ProfissionalResponse, body, {"salao_id": 1})


@router.get("/{profissional_id}", response_model=ProfissionalResponse)
async def obter(profissional_id: str):
    return await crud.obter(db.profissionais, ProfissionalResponse, profissional_id, NAO_ENCONTRADO)


@router.put("/{profissional_id}", response_model=ProfissionalResponse)
async def atualizar(profissional_id: str, body: ProfissionalUpdate):
    return await crud.atualizar(db.profissionais, ProfissionalResponse, profissional_id, body, NAO_ENCONTRADO)


@router.delete("/{profissional_id}", status_code=204)
async def deletar(profissional_id: str):
    await crud.deletar(db.profissionais, profissional_id, NAO_ENCONTRADO)

===== FILE: backend/app/routers/servicos.py =====
from fastapi import APIRouter, Depends, HTTPException
from pymongo import ReturnDocument

from app import crud
from app.db import db, oid
from app.dependencies import get_current_user
from app.schemas.servico import (
    ServicoCreate,
    ServicoInsumoCreate,
    ServicoInsumoResponse,
    ServicoResponse,
    ServicoUpdate,
)

router = APIRouter(prefix="/servicos", tags=["servicos"], dependencies=[Depends(get_current_user)])
NAO_ENCONTRADO = "Serviço não encontrado"


@router.get("/", response_model=list[ServicoResponse])
async def listar():
    return await crud.listar(db.servicos, ServicoResponse)


@router.post("/", response_model=ServicoResponse, status_code=201)
async def criar(body: ServicoCreate):
    return await crud.criar(db.servicos, ServicoResponse, body, {"salao_id": 1})


@router.get("/{servico_id}", response_model=ServicoResponse)
async def obter(servico_id: str):
    return await crud.obter(db.servicos, ServicoResponse, servico_id, NAO_ENCONTRADO)


@router.put("/{servico_id}", response_model=ServicoResponse)
async def atualizar(servico_id: str, body: ServicoUpdate):
    return await crud.atualizar(db.servicos, ServicoResponse, servico_id, body, NAO_ENCONTRADO)


@router.delete("/{servico_id}", status_code=204)
async def deletar(servico_id: str):
    await crud.deletar(db.servicos, servico_id, NAO_ENCONTRADO)
    await db.servico_insumos.delete_many({"servico_id": oid(servico_id)})


# ---------- Insumos consumidos por serviço ----------


async def _relacoes(servico_id) -> list[ServicoInsumoResponse]:
    rels = await db.servico_insumos.find({"servico_id": servico_id}).to_list(200)
    ids = [r["insumo_id"] for r in rels]
    insumos = {i["_id"]: i for i in await db.insumos.find({"_id": {"$in": ids}}).to_list(len(ids) or 1)} if ids else {}
    out = []
    for r in rels:
        ins = insumos.get(r["insumo_id"], {})
        out.append(
            ServicoInsumoResponse.from_mongo(
                {
                    **r,
                    "insumo_nome": ins.get("nome", "—"),
                    "quantidade_atual": ins.get("quantidade_atual", 0),
                    "quantidade_minima_alerta": ins.get("quantidade_minima_alerta", 0),
                }
            )
        )
    return sorted(out, key=lambda x: x.insumo_nome)


@router.get("/{servico_id}/insumos", response_model=list[ServicoInsumoResponse])
async def listar_insumos(servico_id: str):
    await crud.obter(db.servicos, ServicoResponse, servico_id, NAO_ENCONTRADO)
    return await _relacoes(oid(servico_id))


@router.post("/{servico_id}/insumos", response_model=list[ServicoInsumoResponse], status_code=201)
async def vincular_insumo(servico_id: str, body: ServicoInsumoCreate):
    """Cria ou atualiza a quantidade consumida do insumo neste serviço."""
    await crud.obter(db.servicos, ServicoResponse, servico_id, NAO_ENCONTRADO)
    insumo_oid = oid(body.insumo_id, "Insumo não encontrado")
    if await db.insumos.find_one({"_id": insumo_oid}) is None:
        raise HTTPException(status_code=404, detail="Insumo não encontrado")
    await db.servico_insumos.find_one_and_update(
        {"servico_id": oid(servico_id), "insumo_id": insumo_oid},
        {"$set": {"quantidade_utilizada": body.quantidade_utilizada}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return await _relacoes(oid(servico_id))


@router.delete("/{servico_id}/insumos/{insumo_id}", status_code=204)
async def desvincular_insumo(servico_id: str, insumo_id: str):
    res = await db.servico_insumos.delete_one({"servico_id": oid(servico_id), "insumo_id": oid(insumo_id, "Insumo não encontrado")})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Vínculo não encontrado")

===== FILE: backend/app/schemas/__init__.py =====

===== FILE: backend/app/schemas/agendamento.py =====
from datetime import datetime

from pydantic import BaseModel

from app.db import BaseDocument


class AgendamentoResponse(BaseDocument):
    cliente_id: str
    profissional_id: str
    servico_id: str
    data_hora_inicio: datetime
    data_hora_fim: datetime
    status: str
    servico_nome: str = "—"
    cliente_nome: str | None = None
    profissional_nome: str = "—"
    servico_valor: float = 0.0
    alertas_estoque: list[str] = []


class AgendamentoCreate(BaseModel):
    servico_id: str
    profissional_id: str
    cliente_telefone: str
    cliente_nome: str | None = None
    cliente_id: str | None = None
    data_hora_inicio: datetime
    data_hora_fim: datetime | None = None


class AgendamentoUpdate(BaseModel):
    servico_id: str | None = None
    profissional_id: str | None = None
    cliente_id: str | None = None
    data_hora_inicio: datetime | None = None
    data_hora_fim: datetime | None = None
    status: str | None = None

===== FILE: backend/app/schemas/ai.py =====
from datetime import datetime

from pydantic import BaseModel, Field

from app.db import BaseDocument


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None


class ChatMessage(BaseDocument):
    session_id: str
    role: str
    content: str
    criado_em: datetime


class GerarMensagemRequest(BaseModel):
    cliente_nome: str | None = None
    servico: str | None = None
    horario: str | None = None
    tom: str = "carinhoso e profissional"

===== FILE: backend/app/schemas/debito.py =====
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

===== FILE: backend/app/schemas/estoque.py =====
from pydantic import BaseModel


class AlertaEstoqueResponse(BaseModel):
    insumo_id: str
    nome: str
    quantidade_atual: float
    quantidade_minima_alerta: float
    demanda_prevista: float
    tipo: str
    mensagem: str

===== FILE: backend/app/schemas/financeiro.py =====
from datetime import datetime

from pydantic import BaseModel

from app.db import BaseDocument


class FaturamentoResponse(BaseModel):
    total: float
    data_inicio: str
    data_fim: str


class MovimentoCreate(BaseModel):
    tipo: str
    valor: float
    descricao: str


class MovimentoResponse(BaseDocument):
    tipo: str
    valor: float
    descricao: str
    data: datetime


class ResumoFinanceiroResponse(BaseModel):
    entradas: float
    saidas: float
    saldo: float
    lancamentos: list[MovimentoResponse]

===== FILE: backend/app/schemas/insumo.py =====
from pydantic import BaseModel

from app.db import BaseDocument


class InsumoCreate(BaseModel):
    nome: str
    quantidade_atual: float = 0
    quantidade_minima_alerta: float = 0


class InsumoUpdate(BaseModel):
    nome: str | None = None
    quantidade_atual: float | None = None
    quantidade_minima_alerta: float | None = None


class InsumoResponse(BaseDocument):
    nome: str
    quantidade_atual: float
    quantidade_minima_alerta: float

===== FILE: backend/app/schemas/lembrete.py =====
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from app.db import BaseDocument, MongoModel


class LembreteCreate(BaseModel):
    mensagem: str
    canal: str


class LembreteResponse(BaseDocument):
    mensagem: str
    canal: str
    criado_em: datetime


class LembreteInfo(MongoModel):
    mensagem: str | None = None
    gerado_em: datetime | None = None
    enviado_em: datetime | None = None
    canal: str | None = None
    twilio_sid: str | None = None
    erro: str | None = None


class LembreteVesperaResponse(BaseDocument):
    cliente_nome: str | None = None
    cliente_telefone: str
    telefone_e164: str | None = None
    servico_nome: str
    profissional_nome: str
    data_hora_inicio: datetime
    status: str
    lembrete: LembreteInfo = LembreteInfo()


class LembreteMensagemUpdate(BaseModel):
    mensagem: str = Field(min_length=1, max_length=1000)


class EnviarLembreteRequest(BaseModel):
    canal: Literal["twilio", "whatsapp_link"] = "twilio"
    mensagem: str | None = None


class EnvioResultado(BaseModel):
    agendamento_id: str
    ok: bool
    detalhe: str | None = None
    item: LembreteVesperaResponse | None = None


class WhatsAppConfigResponse(BaseModel):
    twilio_configurado: bool
    sandbox: bool
    remetente: str | None = None


class LembretesVesperaIARequest(BaseModel):
    agendamento_ids: list[str] | None = None
    tom: str = "carinhoso e profissional"

===== FILE: backend/app/schemas/profissional.py =====
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

===== FILE: backend/app/schemas/servico.py =====
from pydantic import BaseModel, Field

from app.db import BaseDocument


class ServicoCreate(BaseModel):
    nome: str
    duracao_minutos: int
    valor: float


class ServicoUpdate(BaseModel):
    nome: str | None = None
    duracao_minutos: int | None = None
    valor: float | None = None


class ServicoResponse(BaseDocument):
    nome: str
    duracao_minutos: int
    valor: float


class ServicoInsumoCreate(BaseModel):
    insumo_id: str
    quantidade_utilizada: float = Field(gt=0)


class ServicoInsumoResponse(BaseDocument):
    servico_id: str
    insumo_id: str
    insumo_nome: str = "—"
    quantidade_utilizada: float
    quantidade_atual: float = 0
    quantidade_minima_alerta: float = 0

===== FILE: backend/app/schemas/usuario.py =====
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

===== FILE: backend/app/services/__init__.py =====

===== FILE: backend/app/services/ai.py =====
from typing import AsyncIterator

from emergentintegrations.llm.chat import LlmChat, StreamDone, TextDelta, UserMessage

from app import config
from app.db import db, janela_dia, local

PROVIDER = "anthropic"
MODEL = "claude-sonnet-4-5-20250929"


def novo_chat(session_id: str, system_message: str, historico: list[dict] | None = None) -> LlmChat:
    initial = [{"role": "system", "content": system_message}, *(historico or [])]
    return LlmChat(
        api_key=config.EMERGENT_LLM_KEY,
        session_id=session_id,
        system_message=system_message,
        initial_messages=initial,
    ).with_model(PROVIDER, MODEL)


async def stream_texto(chat: LlmChat, texto: str) -> AsyncIterator[str]:
    async for ev in chat.stream_message(UserMessage(text=texto)):
        if isinstance(ev, TextDelta):
            yield ev.content
        elif isinstance(ev, StreamDone):
            break


async def gerar_texto(session_id: str, system_message: str, pedido: str) -> str:
    chat = novo_chat(session_id, system_message)
    return "".join([parte async for parte in stream_texto(chat, pedido)]).strip()


async def contexto_salao(user) -> str:
    hoje, amanha = janela_dia(0)

    servicos = await db.servicos.find().to_list(50)
    profissionais = await db.profissionais.find().to_list(50)
    insumos = await db.insumos.find().to_list(100)
    agendamentos = await db.agendamentos.find(
        {"data_hora_inicio": {"$gte": hoje, "$lt": amanha}}
    ).sort("data_hora_inicio", 1).to_list(50)

    srv_map = {s["_id"]: s for s in servicos}
    prof_map = {p["_id"]: p for p in profissionais}
    cli_ids = [a["cliente_id"] for a in agendamentos]
    clientes = {c["_id"]: c for c in await db.clientes.find({"_id": {"$in": cli_ids}}).to_list(50)} if cli_ids else {}

    linhas_ag = [
        f"- {local(a['data_hora_inicio']).strftime('%H:%M')} — "
        f"{clientes.get(a['cliente_id'], {}).get('nome') or 'Cliente'} · "
        f"{srv_map.get(a['servico_id'], {}).get('nome', '?')} com "
        f"{prof_map.get(a['profissional_id'], {}).get('nome', '?')} ({a['status']})"
        for a in agendamentos
    ] or ["- nenhum agendamento hoje"]
    linhas_srv = [f"- {s['nome']}: {s['duracao_minutos']} min, R$ {s['valor']:.2f}" for s in servicos] or ["- nenhum"]
    linhas_prof = [f"- {p['nome']} ({p.get('especialidades') or 'geral'})" for p in profissionais] or ["- nenhum"]
    baixos = [
        f"- {i['nome']}: {i['quantidade_atual']} un (mínimo {i['quantidade_minima_alerta']})"
        for i in insumos
        if i["quantidade_atual"] <= i["quantidade_minima_alerta"]
    ] or ["- tudo em dia"]

    return (
        "Você é o Assistente ELO, a inteligência do sistema de gestão ELO Beauty Care para salões de beleza. "
        f"Você conversa com {user.nome}, responsável pelo espaço \"{user.business or 'ELO Beauty Care'}\""
        f"{' em ' + user.city if user.city else ''}. "
        f"Hoje é {hoje.strftime('%d/%m/%Y')} (fuso {config.TIMEZONE}); horários abaixo já estão no horário local. "
        "Seja acolhedor, direto e prático. Responda sempre em português do Brasil, em frases curtas, "
        "sem markdown pesado (pode usar listas simples com '-'). Ajude com agenda, atendimento ao cliente, "
        "mensagens para WhatsApp, estoque, finanças e organização do salão. "
        "Use os dados abaixo quando forem relevantes; se não souber algo, diga que não tem a informação.\n\n"
        f"AGENDA DE HOJE:\n" + "\n".join(linhas_ag) + "\n\n"
        f"SERVIÇOS OFERECIDOS:\n" + "\n".join(linhas_srv) + "\n\n"
        f"EQUIPE:\n" + "\n".join(linhas_prof) + "\n\n"
        f"INSUMOS COM ESTOQUE BAIXO:\n" + "\n".join(baixos)
    )


def prompt_mensagem_whatsapp(
    user,
    tom: str,
    *,
    cliente_nome: str | None = None,
    servico: str | None = None,
    horario: str | None = None,
    profissional: str | None = None,
    vespera: bool = False,
) -> tuple[str, str]:
    system = (
        "Você redige mensagens curtas de WhatsApp para clientes de um salão de beleza chamado "
        f"\"{user.business or 'ELO Beauty Care'}\". Escreva em português do Brasil, em primeira pessoa do salão, "
        f"com no máximo 3 frases, tom {tom}, no máximo 1 emoji. Responda APENAS com o texto da mensagem, "
        "sem aspas, sem explicações, sem assinatura."
    )
    detalhes = [
        f"nome da cliente: {cliente_nome}" if cliente_nome else None,
        f"serviço: {servico}" if servico else None,
        f"horário: {horario}" if horario else None,
        f"profissional que vai atender: {profissional}" if profissional else None,
    ]
    pedido = (
        "Escreva um lembrete de véspera: o atendimento é AMANHÃ. Peça para a cliente confirmar presença respondendo a mensagem."
        if vespera
        else "Escreva um lembrete de atendimento pedindo confirmação de presença."
    )
    if any(detalhes):
        pedido += " Detalhes: " + "; ".join(d for d in detalhes if d) + "."
    return system, pedido

===== FILE: backend/app/services/auth.py =====
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

===== FILE: backend/app/services/lembretes.py =====
"""Lembretes de véspera: agendamentos de amanhã + geração/envio de mensagens."""

from bson import ObjectId
from fastapi import HTTPException
from pymongo import ReturnDocument

from app.db import db, janela_dia, now, oid
from app.schemas.lembrete import LembreteVesperaResponse
from app.services.whatsapp import normalizar_telefone

STATUS_ATIVOS = ("confirmado", "pendente")


async def _mapa(col, ids: list[ObjectId]) -> dict:
    return {d["_id"]: d for d in await col.find({"_id": {"$in": ids}}).to_list(len(ids) or 1)} if ids else {}


async def _montar(docs: list[dict]) -> list[LembreteVesperaResponse]:
    servicos = await _mapa(db.servicos, [d["servico_id"] for d in docs])
    clientes = await _mapa(db.clientes, [d["cliente_id"] for d in docs])
    profs = await _mapa(db.profissionais, [d["profissional_id"] for d in docs])
    itens = []
    for d in docs:
        cliente = clientes.get(d["cliente_id"], {})
        telefone = cliente.get("telefone") or ""
        itens.append(
            LembreteVesperaResponse.from_mongo(
                {
                    **d,
                    "cliente_nome": cliente.get("nome"),
                    "cliente_telefone": telefone,
                    "telefone_e164": normalizar_telefone(telefone),
                    "servico_nome": servicos.get(d["servico_id"], {}).get("nome", "—"),
                    "profissional_nome": profs.get(d["profissional_id"], {}).get("nome", "—"),
                    "lembrete": d.get("lembrete") or {},
                }
            )
        )
    return itens


async def listar_amanha(ids: list[str] | None = None) -> list[LembreteVesperaResponse]:
    inicio, fim = janela_dia(1)
    filtro: dict = {"data_hora_inicio": {"$gte": inicio, "$lt": fim}, "status": {"$in": list(STATUS_ATIVOS)}}
    if ids:
        filtro["_id"] = {"$in": [oid(i) for i in ids]}
    docs = await db.agendamentos.find(filtro).sort("data_hora_inicio", 1).to_list(200)
    return await _montar(docs)


async def obter(agendamento_id: str) -> LembreteVesperaResponse:
    doc = await db.agendamentos.find_one({"_id": oid(agendamento_id, "Agendamento não encontrado")})
    if doc is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return (await _montar([doc]))[0]


async def salvar_mensagem(agendamento_id: str, mensagem: str) -> LembreteVesperaResponse:
    doc = await db.agendamentos.find_one_and_update(
        {"_id": oid(agendamento_id, "Agendamento não encontrado")},
        {"$set": {"lembrete.mensagem": mensagem.strip(), "lembrete.gerado_em": now()}},
        return_document=ReturnDocument.AFTER,
    )
    if doc is None:
        raise HTTPException(status_code=404, detail="Agendamento não encontrado")
    return (await _montar([doc]))[0]


async def registrar_envio(item: LembreteVesperaResponse, canal: str, mensagem: str, twilio_sid: str | None = None):
    campos = {"lembrete.enviado_em": now(), "lembrete.canal": canal, "lembrete.twilio_sid": twilio_sid, "lembrete.erro": None}
    doc = await db.agendamentos.find_one_and_update(
        {"_id": ObjectId(item.id)}, {"$set": campos}, return_document=ReturnDocument.AFTER
    )
    await db.lembretes.insert_one(
        {
            "mensagem": mensagem,
            "canal": f"{canal}:{item.telefone_e164 or item.cliente_telefone}",
            "criado_em": now(),
            "agendamento_id": ObjectId(item.id),
            "salao_id": 1,
        }
    )
    return (await _montar([doc]))[0]


async def registrar_erro(item: LembreteVesperaResponse, erro: str) -> LembreteVesperaResponse:
    doc = await db.agendamentos.find_one_and_update(
        {"_id": ObjectId(item.id)}, {"$set": {"lembrete.erro": erro}}, return_document=ReturnDocument.AFTER
    )
    return (await _montar([doc]))[0]

===== FILE: backend/app/services/whatsapp.py =====
"""Envio de WhatsApp via Twilio (REST API, sem SDK).

Ativa automaticamente quando TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN e
TWILIO_WHATSAPP_FROM estiverem preenchidos no backend/.env.
Sem credenciais, o app continua funcionando com links wa.me.
"""

import re
from urllib.parse import quote

import httpx

from app import config

SANDBOX_FROM = "whatsapp:+14155238886"
TWILIO_API = "https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"


class EnvioWhatsAppError(Exception):
    pass


def configurado() -> bool:
    return bool(config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN and config.TWILIO_WHATSAPP_FROM)


def usando_sandbox() -> bool:
    return config.TWILIO_WHATSAPP_FROM == SANDBOX_FROM


def remetente_mascarado() -> str | None:
    if not config.TWILIO_WHATSAPP_FROM:
        return None
    numero = config.TWILIO_WHATSAPP_FROM.replace("whatsapp:", "")
    return f"{numero[:4]}…{numero[-4:]}" if len(numero) > 8 else numero


def normalizar_telefone(telefone: str | None) -> str | None:
    """Converte '55 42 99999-0000', '(42) 99999-0000' ou '5542999990000' para E.164 (+5542999990000)."""
    digitos = re.sub(r"\D", "", telefone or "")
    if not digitos:
        return None
    if len(digitos) in (10, 11):
        digitos = "55" + digitos
    if not 12 <= len(digitos) <= 15:
        return None
    return "+" + digitos


def link_wa(telefone_e164: str, mensagem: str) -> str:
    return f"https://wa.me/{telefone_e164.lstrip('+')}?text={quote(mensagem)}"


async def enviar(telefone_e164: str, mensagem: str) -> str:
    """Envia a mensagem e devolve o SID do Twilio."""
    if not configurado():
        raise EnvioWhatsAppError("Twilio não configurado. Preencha TWILIO_* no backend/.env.")
    url = TWILIO_API.format(sid=config.TWILIO_ACCOUNT_SID)
    payload = {"From": config.TWILIO_WHATSAPP_FROM, "To": f"whatsapp:{telefone_e164}", "Body": mensagem}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            r = await client.post(url, auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN), data=payload)
    except httpx.HTTPError as exc:
        raise EnvioWhatsAppError(f"Falha de rede ao contatar o Twilio: {exc}") from exc
    if r.status_code >= 400:
        try:
            detalhe = r.json().get("message")
        except ValueError:
            detalhe = r.text
        raise EnvioWhatsAppError(detalhe or f"Twilio respondeu HTTP {r.status_code}")
    return r.json()["sid"]

===== FILE: backend/pytest.ini =====
[pytest]
# Fixed 2 xdist workers (deterministic, not reliant on the agent passing -n). loadscope pins each test
# class/module to one worker — generated suites share one preview backend and assume sequential shared
# state — so it parallelizes across classes/modules without cross-test races.
# AGENT: do NOT modify addopts; keep exactly -n 2 --dist loadscope and run only what is configured here.
# Serial = `-n 0` (NOT `-p no:xdist`, which errors because addopts still passes -n/--dist). A custom `-n`
# option in your own pytest setup collides with xdist's -n — rename it.
required_plugins = pytest-xdist
addopts = -n 2 --dist loadscope

===== FILE: backend/requirements.txt =====
fastapi==0.110.1
uvicorn==0.25.0
boto3>=1.34.129
requests-oauthlib>=2.0.0
cryptography>=42.0.8
python-dotenv>=1.0.1
pymongo==4.6.3
pydantic>=2.6.4
email-validator>=2.2.0
pyjwt>=2.10.1
bcrypt==4.1.3
passlib>=1.7.4
tzdata>=2024.2
motor==3.3.1
pytest>=8.0.0
pytest-xdist>=3.6.0
black>=24.1.1
isort>=5.13.2
flake8>=7.0.0
mypy>=1.8.0
python-jose>=3.3.0
requests>=2.31.0
pandas>=2.2.0
numpy>=1.26.0
python-multipart>=0.0.9
jq>=1.6.0
typer>=0.9.0
emergentintegrations==0.2.1
httpx>=0.27.0

===== FILE: backend/server.py =====
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
    await db.servico_insumos.create_index([("servico_id", 1), ("insumo_id", 1)], unique=True)
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

    if await db.servico_insumos.count_documents({}) == 0:
        servicos_map = {s["nome"]: s["_id"] async for s in db.servicos.find()}
        insumos_map = {i["nome"]: i["_id"] async for i in db.insumos.find()}
        vinculos = [
            ("Corte Feminino", "Shampoo Profissional", 1),
            ("Escova", "Shampoo Profissional", 1),
            ("Coloração", "Coloração Loiro", 1),
            ("Coloração", "Máscara Hidratante", 1),
            ("Manicure", "Esmalte Rosa", 1),
        ]
        docs = [
            {"servico_id": servicos_map[s], "insumo_id": insumos_map[i], "quantidade_utilizada": q}
            for s, i, q in vinculos
            if s in servicos_map and i in insumos_map
        ]
        if docs:
            await db.servico_insumos.insert_many(docs)

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

===== FILE: backend/tests/backend_test.py =====
"""ELO Beauty Care - Backend regression tests (MongoDB migration + AI + Google session)"""
import os
import time
import json
import uuid
import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BASE_URL:
    # fallback: read from frontend .env
    with open("/app/frontend/.env") as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                BASE_URL = line.split("=", 1)[1].strip()
                break
BASE_URL = BASE_URL.rstrip("/")
API = f"{BASE_URL}/api"

ADMIN_EMAIL = "admin@elo.beauty"
ADMIN_PASS = "elo123456"


# -------------------- Fixtures --------------------
@pytest.fixture(scope="session")
def admin_token():
    r = requests.post(f"{API}/auth/login", json={"email": ADMIN_EMAIL, "senha": ADMIN_PASS}, timeout=15)
    assert r.status_code == 200, f"admin login failed: {r.status_code} {r.text}"
    return r.json()["access_token"]


@pytest.fixture(scope="session")
def auth_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}


@pytest.fixture(scope="session")
def google_session_token():
    """Create a simulated Google session via mongosh per auth_testing.md"""
    import subprocess
    token = f"test_session_{int(time.time())}_{uuid.uuid4().hex[:6]}"
    script = f"""
use('test_database');
var u = db.usuarios.findOneAndUpdate(
  {{email: 'google.tester@example.com'}},
  {{$setOnInsert: {{email: 'google.tester@example.com', nome: 'Google Tester', business: 'Studio Teste', city: null, picture: 'https://via.placeholder.com/150', criado_em: new Date()}}}},
  {{upsert: true, returnDocument: 'after'}}
);
db.user_sessions.insertOne({{user_id: u._id.toString(), session_token: '{token}', expires_at: new Date(Date.now() + 7*24*60*60*1000), created_at: new Date()}});
print('OK');
"""
    result = subprocess.run(["mongosh", "--quiet", "--eval", script], capture_output=True, text=True, timeout=30)
    assert "OK" in result.stdout, f"mongosh failed: {result.stdout} {result.stderr}"
    return token


# -------------------- Auth --------------------
class TestAuth:
    def test_login_admin(self, admin_token):
        assert isinstance(admin_token, str) and len(admin_token) > 20

    def test_me_returns_string_id_no_underscore(self, auth_headers):
        r = requests.get(f"{API}/auth/me", headers=auth_headers, timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert "id" in data and isinstance(data["id"], str)
        assert "_id" not in data
        assert data["email"] == ADMIN_EMAIL

    def test_login_invalid(self):
        r = requests.post(f"{API}/auth/login", json={"email": ADMIN_EMAIL, "senha": "bad"}, timeout=10)
        assert r.status_code == 401

    def test_register_duplicate_email(self):
        r = requests.post(f"{API}/auth/register", json={"email": "qa@elo.beauty", "senha": "qa123456", "nome": "QA"}, timeout=10)
        assert r.status_code == 409

    def test_register_short_password(self):
        r = requests.post(f"{API}/auth/register", json={"email": f"short_{uuid.uuid4().hex[:6]}@example.com", "senha": "12345", "nome": "X"}, timeout=10)
        assert r.status_code == 422

    def test_register_new_and_login(self):
        email = f"TEST_{uuid.uuid4().hex[:8]}@elo.example.com"
        r = requests.post(f"{API}/auth/register", json={"email": email, "senha": "senha123", "nome": "Novo"}, timeout=10)
        assert r.status_code == 201, r.text
        data = r.json()
        assert "access_token" in data
        # cleanup
        import subprocess
        subprocess.run(["mongosh", "--quiet", "--eval", f"use('test_database'); db.usuarios.deleteOne({{email: '{email}'}});"], capture_output=True, timeout=15)

    def test_update_me(self, auth_headers):
        r = requests.put(f"{API}/auth/me", headers=auth_headers, json={"business": "ELO Beauty QA", "city": "SP"}, timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert data["business"] == "ELO Beauty QA"
        assert data["city"] == "SP"
        assert "_id" not in data


# -------------------- Google session (simulated) --------------------
class TestGoogleSession:
    def test_me_via_bearer_session_token(self, google_session_token):
        r = requests.get(f"{API}/auth/me", headers={"Authorization": f"Bearer {google_session_token}"}, timeout=10)
        assert r.status_code == 200
        assert r.json()["email"] == "google.tester@example.com"
        assert "_id" not in r.json()

    def test_me_via_cookie(self, google_session_token):
        r = requests.get(f"{API}/auth/me", cookies={"session_token": google_session_token}, timeout=10)
        assert r.status_code == 200

    def test_session_invalid(self):
        r = requests.post(f"{API}/auth/session", json={"session_id": "invalid_xyz"}, timeout=15)
        assert r.status_code == 401

    def test_logout_invalidates_session(self, google_session_token):
        r = requests.post(f"{API}/auth/logout", headers={"Authorization": f"Bearer {google_session_token}"}, timeout=10)
        assert r.status_code in (200, 204)
        r2 = requests.get(f"{API}/auth/me", headers={"Authorization": f"Bearer {google_session_token}"}, timeout=10)
        assert r2.status_code == 401


# -------------------- CRUD generic --------------------
class TestServicos:
    def test_crud_full(self, auth_headers):
        r = requests.get(f"{API}/servicos/", headers=auth_headers, timeout=10)
        assert r.status_code == 200 and isinstance(r.json(), list)

        payload = {"nome": "TEST_Servico", "duracao_minutos": 30, "valor": 50.0, "ativo": True}
        r = requests.post(f"{API}/servicos/", headers=auth_headers, json=payload, timeout=10)
        assert r.status_code == 201, r.text
        sid = r.json()["id"]
        assert isinstance(sid, str)
        assert "_id" not in r.json()

        r = requests.get(f"{API}/servicos/{sid}", headers=auth_headers, timeout=10)
        assert r.status_code == 200 and r.json()["nome"] == "TEST_Servico"

        r = requests.put(f"{API}/servicos/{sid}", headers=auth_headers, json={"valor": 75.0}, timeout=10)
        assert r.status_code == 200 and r.json()["valor"] == 75.0

        r = requests.delete(f"{API}/servicos/{sid}", headers=auth_headers, timeout=10)
        assert r.status_code == 204

        r = requests.get(f"{API}/servicos/{sid}", headers=auth_headers, timeout=10)
        assert r.status_code == 404

    def test_invalid_id(self, auth_headers):
        r = requests.get(f"{API}/servicos/abc", headers=auth_headers, timeout=10)
        assert r.status_code in (400, 404, 422)


class TestInsumos:
    def test_crud(self, auth_headers):
        r = requests.get(f"{API}/insumos/", headers=auth_headers, timeout=10)
        assert r.status_code == 200
        payload = {"nome": "TEST_Insumo", "unidade": "un", "quantidade": 10, "minimo": 2, "custo": 5.0}
        r = requests.post(f"{API}/insumos/", headers=auth_headers, json=payload, timeout=10)
        assert r.status_code == 201, r.text
        iid = r.json()["id"]
        r = requests.delete(f"{API}/insumos/{iid}", headers=auth_headers, timeout=10)
        assert r.status_code == 204


class TestProfissionais:
    def test_crud(self, auth_headers):
        r = requests.get(f"{API}/profissionais/", headers=auth_headers, timeout=10)
        assert r.status_code == 200
        payload = {"nome": "TEST_Prof", "especialidade": "Testes", "ativo": True}
        r = requests.post(f"{API}/profissionais/", headers=auth_headers, json=payload, timeout=10)
        assert r.status_code == 201, r.text
        pid = r.json()["id"]
        r = requests.delete(f"{API}/profissionais/{pid}", headers=auth_headers, timeout=10)
        assert r.status_code == 204


# -------------------- Agendamentos --------------------
class TestAgendamentos:
    def test_list(self, auth_headers):
        r = requests.get(f"{API}/agendamentos/", headers=auth_headers, timeout=10)
        assert r.status_code == 200 and isinstance(r.json(), list)
        if r.json():
            item = r.json()[0]
            assert "servico_nome" in item and "cliente_nome" in item and "profissional_nome" in item
            assert "_id" not in item
            # UTC Z suffix
            if "inicio" in item:
                assert isinstance(item["inicio"], str)

    def test_create_conflict_and_conclude(self, auth_headers):
        servicos = requests.get(f"{API}/servicos/", headers=auth_headers).json()
        profs = requests.get(f"{API}/profissionais/", headers=auth_headers).json()
        assert servicos and profs
        from datetime import datetime, timezone, timedelta
        start = (datetime.now(timezone.utc) + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
        payload = {
            "servico_id": servicos[0]["id"],
            "profissional_id": profs[0]["id"],
            "cliente_nome": "TEST_Cli",
            "cliente_telefone": "11999999999",
            "data_hora_inicio": start.isoformat().replace("+00:00", "Z"),
        }
        r = requests.post(f"{API}/agendamentos/", headers=auth_headers, json=payload, timeout=10)
        assert r.status_code == 201, r.text
        aid = r.json()["id"]

        # conflict
        r2 = requests.post(f"{API}/agendamentos/", headers=auth_headers, json=payload, timeout=10)
        assert r2.status_code == 409, f"expected 409 conflict, got {r2.status_code}: {r2.text}"

        # concluir
        r3 = requests.patch(f"{API}/agendamentos/{aid}/concluir", headers=auth_headers, timeout=10)
        assert r3.status_code == 200
        assert r3.json().get("status") == "concluido"

        # delete
        r4 = requests.delete(f"{API}/agendamentos/{aid}", headers=auth_headers, timeout=10)
        assert r4.status_code == 204


# -------------------- Estoque / Financeiro / Dashboard / Lembretes / Debitos --------------------
class TestOther:
    def test_estoque_alertas(self, auth_headers):
        r = requests.get(f"{API}/estoque/alertas", headers=auth_headers, timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)

    def test_financeiro_resumo(self, auth_headers):
        r = requests.get(f"{API}/financeiro/resumo", headers=auth_headers, timeout=10)
        assert r.status_code == 200
        d = r.json()
        for k in ("entradas", "saidas", "saldo", "lancamentos"):
            assert k in d, f"missing {k}"

    def test_financeiro_lancamento(self, auth_headers):
        p = {"tipo": "entrada", "descricao": "TEST_lanc", "valor": 100.0}
        r = requests.post(f"{API}/financeiro/lancamentos", headers=auth_headers, json=p, timeout=10)
        assert r.status_code in (200, 201), r.text

    def test_dashboard_financeiro(self, auth_headers):
        from datetime import date, timedelta
        di = (date.today() - timedelta(days=30)).isoformat()
        df = date.today().isoformat()
        r = requests.get(f"{API}/dashboard/financeiro", headers=auth_headers, params={"data_inicio": di, "data_fim": df}, timeout=10)
        assert r.status_code == 200

    def test_lembretes_crud(self, auth_headers):
        r = requests.get(f"{API}/lembretes/", headers=auth_headers, timeout=10)
        assert r.status_code == 200
        p = {"cliente_nome": "TEST_C", "telefone": "1199", "mensagem": "oi", "canal": "whatsapp"}
        r = requests.post(f"{API}/lembretes/", headers=auth_headers, json=p, timeout=10)
        assert r.status_code in (200, 201), r.text

    def test_debitos(self, auth_headers):
        r = requests.get(f"{API}/debitos/", headers=auth_headers, timeout=10)
        assert r.status_code == 200


# -------------------- AI (SSE) --------------------
class TestAI:
    def _consume_sse(self, response, timeout=25):
        """Parse SSE events; return (session_id, full_text, done)."""
        session_id = None
        full = []
        done = False
        start = time.time()
        for raw in response.iter_lines(decode_unicode=True):
            if time.time() - start > timeout:
                break
            if not raw:
                continue
            if raw.startswith("data:"):
                payload = raw[5:].strip()
                if not payload:
                    continue
                try:
                    evt = json.loads(payload)
                except Exception:
                    continue
                if "session_id" in evt and not session_id:
                    session_id = evt["session_id"]
                if "delta" in evt:
                    full.append(evt["delta"])
                if evt.get("done"):
                    done = True
                    break
        return session_id, "".join(full), done

    def test_chat_requires_auth(self):
        r = requests.post(f"{API}/ai/chat", json={"message": "oi"}, timeout=10)
        assert r.status_code == 401

    def test_chat_stream_and_multiturn(self, auth_headers):
        with requests.post(f"{API}/ai/chat", headers=auth_headers, json={"message": "Meu nome é Carlos, lembre-se disso."}, stream=True, timeout=60) as r:
            assert r.status_code == 200
            assert "text/event-stream" in r.headers.get("content-type", "")
            sid, text, done = self._consume_sse(r)
            assert sid, "no session_id received"
            assert len(text) > 0, "no delta text"
            assert done

        # multi-turn
        with requests.post(f"{API}/ai/chat", headers=auth_headers, json={"message": "Qual é o meu nome?", "session_id": sid}, stream=True, timeout=60) as r2:
            assert r2.status_code == 200
            _, text2, done2 = self._consume_sse(r2)
            assert done2
            assert "carlos" in text2.lower(), f"context lost, got: {text2[:200]}"

        # history
        r3 = requests.get(f"{API}/ai/chat/{sid}/messages", headers=auth_headers, timeout=10)
        assert r3.status_code == 200
        msgs = r3.json()
        assert isinstance(msgs, list) and len(msgs) >= 4
        roles = [m.get("role") for m in msgs]
        assert "user" in roles and "assistant" in roles

    def test_gerar_mensagem(self, auth_headers):
        payload = {"cliente_nome": "Maria", "servico": "Manicure", "horario": "amanhã 14h"}
        with requests.post(f"{API}/ai/gerar-mensagem", headers=auth_headers, json=payload, stream=True, timeout=60) as r:
            assert r.status_code == 200
            _, text, done = self._consume_sse(r)
            assert done and len(text) > 10
            assert "maria" in text.lower()

===== FILE: backend/tests/test_lembretes_insumos.py =====
"""Iteration 2: WhatsApp reminders (véspera) + Insumos por serviço + dedução de estoque."""
import json
import os
import time
from datetime import datetime, timedelta, timezone

import pytest
import requests

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL")
if not BASE_URL:
    with open("/app/frontend/.env") as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                BASE_URL = line.split("=", 1)[1].strip()
                break
BASE_URL = BASE_URL.rstrip("/")
API = f"{BASE_URL}/api"

ADMIN = {"email": "admin@elo.beauty", "senha": "elo123456"}


@pytest.fixture(scope="module")
def headers():
    r = requests.post(f"{API}/auth/login", json=ADMIN, timeout=15)
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


# ---------------- LEMBRETES / CONFIG ----------------

class TestLembretesConfig:
    def test_config(self, headers):
        r = requests.get(f"{API}/lembretes/config", headers=headers, timeout=10)
        assert r.status_code == 200
        d = r.json()
        assert d["twilio_configurado"] is False
        assert d["sandbox"] is True
        assert d["remetente"] and "…" in d["remetente"]

    def test_enviar_todos_503(self, headers):
        r = requests.post(f"{API}/lembretes/vespera/enviar-todos", headers=headers, timeout=10)
        assert r.status_code == 503


# ---------------- LEMBRETES DE VÉSPERA ----------------

def _amanha_utc(hour_utc: int, minute: int = 0):
    now_utc = datetime.now(timezone.utc)
    tomorrow = (now_utc + timedelta(days=1)).replace(hour=hour_utc, minute=minute, second=0, microsecond=0)
    return tomorrow


class TestVespera:
    def test_listar_vespera_seed(self, headers):
        r = requests.get(f"{API}/lembretes/vespera", headers=headers, timeout=15)
        assert r.status_code == 200
        items = r.json()
        assert isinstance(items, list) and len(items) >= 1
        item = items[0]
        for k in ("id", "cliente_nome", "cliente_telefone", "telefone_e164",
                  "servico_nome", "profissional_nome", "data_hora_inicio", "status", "lembrete"):
            assert k in item, f"campo faltando: {k}"
        assert item["data_hora_inicio"].endswith("Z")
        assert item["telefone_e164"] is None or item["telefone_e164"].startswith("+55")
        assert item["status"] != "concluido"
        assert "_id" not in item

    def test_put_mensagem_vazia_422(self, headers):
        items = requests.get(f"{API}/lembretes/vespera", headers=headers).json()
        assert items
        aid = items[0]["id"]
        r = requests.put(f"{API}/lembretes/vespera/{aid}", headers=headers, json={"mensagem": ""}, timeout=10)
        assert r.status_code == 422

    def test_put_mensagem_ok_and_persistence(self, headers):
        items = requests.get(f"{API}/lembretes/vespera", headers=headers).json()
        aid = items[0]["id"]
        msg = "TEST: Olá! Lembrete do seu horário amanhã."
        r = requests.put(f"{API}/lembretes/vespera/{aid}", headers=headers, json={"mensagem": msg}, timeout=10)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["lembrete"]["mensagem"] == msg
        assert d["lembrete"]["gerado_em"].endswith("Z")
        # persist
        items2 = requests.get(f"{API}/lembretes/vespera", headers=headers).json()
        found = [i for i in items2 if i["id"] == aid][0]
        assert found["lembrete"]["mensagem"] == msg

    def test_put_id_inexistente_404(self, headers):
        r = requests.put(f"{API}/lembretes/vespera/000000000000000000000000",
                         headers=headers, json={"mensagem": "x"}, timeout=10)
        assert r.status_code == 404

    def test_enviar_whatsapp_link_ok(self, headers):
        items = requests.get(f"{API}/lembretes/vespera", headers=headers).json()
        aid = items[0]["id"]
        # ensure has message
        requests.put(f"{API}/lembretes/vespera/{aid}", headers=headers,
                     json={"mensagem": "TEST: link wa"}, timeout=10)
        r = requests.post(f"{API}/lembretes/vespera/{aid}/enviar",
                          headers=headers, json={"canal": "whatsapp_link"}, timeout=10)
        assert r.status_code == 200, r.text
        d = r.json()
        assert d["ok"] is True
        assert d["item"]["lembrete"]["canal"] == "whatsapp_link"
        assert d["item"]["lembrete"]["enviado_em"] is not None
        # aparece em /lembretes/
        lst = requests.get(f"{API}/lembretes/", headers=headers).json()
        assert any(lb.get("canal", "").startswith("whatsapp_link:") for lb in lst)

    def test_enviar_twilio_503(self, headers):
        items = requests.get(f"{API}/lembretes/vespera", headers=headers).json()
        aid = items[0]["id"]
        r = requests.post(f"{API}/lembretes/vespera/{aid}/enviar",
                          headers=headers, json={"canal": "twilio"}, timeout=10)
        assert r.status_code == 503


# ---------------- SSE: gerar lembretes véspera com IA ----------------

def _consume_sse(response, timeout=45):
    events = []
    start = time.time()
    for raw in response.iter_lines(decode_unicode=True):
        if time.time() - start > timeout:
            break
        if not raw or not raw.startswith("data:"):
            continue
        try:
            evt = json.loads(raw[5:].strip())
        except Exception:
            continue
        events.append(evt)
        if evt.get("done"):
            break
    return events


class TestAILembretes:
    def test_sse_completo(self, headers):
        items = requests.get(f"{API}/lembretes/vespera", headers=headers).json()
        total_esperado = len(items)
        assert total_esperado >= 1
        with requests.post(f"{API}/ai/lembretes-vespera", headers=headers, json={},
                           stream=True, timeout=90) as r:
            assert r.status_code == 200
            assert "text/event-stream" in r.headers.get("content-type", "")
            evts = _consume_sse(r, timeout=60)
        assert evts, "no SSE events"
        assert evts[0].get("total") == total_esperado
        msgs = [e for e in evts if "agendamento_id" in e and "mensagem" in e]
        assert len(msgs) >= 1
        assert evts[-1].get("done") is True
        # verify persisted
        items2 = requests.get(f"{API}/lembretes/vespera", headers=headers).json()
        with_msg = [i for i in items2 if i["lembrete"].get("mensagem")]
        assert len(with_msg) >= 1

    def test_sse_single_id(self, headers):
        items = requests.get(f"{API}/lembretes/vespera", headers=headers).json()
        aid = items[0]["id"]
        with requests.post(f"{API}/ai/lembretes-vespera", headers=headers,
                           json={"agendamento_ids": [aid]}, stream=True, timeout=90) as r:
            assert r.status_code == 200
            evts = _consume_sse(r, timeout=45)
        assert evts[0].get("total") == 1
        assert any(e.get("agendamento_id") == aid for e in evts)


# ---------------- INSUMOS POR SERVIÇO ----------------

class TestServicoInsumos:
    def _find_servico(self, headers, name_contains):
        srvs = requests.get(f"{API}/servicos/", headers=headers).json()
        for s in srvs:
            if name_contains.lower() in s["nome"].lower():
                return s
        return None

    def test_seed_vinculos(self, headers):
        for nome, insumo_esperado in [("Corte", "Shampoo"), ("Escova", "Shampoo"),
                                       ("Manicure", "Esmalte")]:
            s = self._find_servico(headers, nome)
            if s is None:
                continue
            r = requests.get(f"{API}/servicos/{s['id']}/insumos", headers=headers, timeout=10)
            assert r.status_code == 200
            rels = r.json()
            assert any(insumo_esperado.lower() in x["insumo_nome"].lower() for x in rels), \
                f"{nome} deveria ter vínculo com {insumo_esperado}: {rels}"
            for rel in rels:
                assert "_id" not in rel
                assert "insumo_nome" in rel
                assert "quantidade_utilizada" in rel
                assert "quantidade_atual" in rel

    def test_post_upsert_and_validation(self, headers):
        # Cria serviço TEST
        r = requests.post(f"{API}/servicos/", headers=headers,
                          json={"nome": "TEST_ServVinc", "duracao_minutos": 30, "valor": 10.0}, timeout=10)
        sid = r.json()["id"]
        # cria insumo TEST
        r = requests.post(f"{API}/insumos/", headers=headers,
                          json={"nome": "TEST_Insumo_Vinc", "unidade": "un",
                                "quantidade_atual": 5.0, "quantidade_minima_alerta": 2.0, "custo": 1.0}, timeout=10)
        iid = r.json()["id"]
        try:
            # quantidade inválida
            r = requests.post(f"{API}/servicos/{sid}/insumos", headers=headers,
                              json={"insumo_id": iid, "quantidade_utilizada": 0}, timeout=10)
            assert r.status_code == 422

            # insumo inexistente
            r = requests.post(f"{API}/servicos/{sid}/insumos", headers=headers,
                              json={"insumo_id": "000000000000000000000000", "quantidade_utilizada": 1}, timeout=10)
            assert r.status_code == 404

            # cria (201) — retorna list
            r = requests.post(f"{API}/servicos/{sid}/insumos", headers=headers,
                              json={"insumo_id": iid, "quantidade_utilizada": 1.5}, timeout=10)
            assert r.status_code == 201, r.text
            data = r.json()
            assert isinstance(data, list) and len(data) == 1
            assert data[0]["quantidade_utilizada"] == 1.5

            # upsert (mesmo insumo) — não duplica
            r = requests.post(f"{API}/servicos/{sid}/insumos", headers=headers,
                              json={"insumo_id": iid, "quantidade_utilizada": 2.5}, timeout=10)
            assert r.status_code == 201
            assert len(r.json()) == 1
            assert r.json()[0]["quantidade_utilizada"] == 2.5

            # DELETE
            r = requests.delete(f"{API}/servicos/{sid}/insumos/{iid}", headers=headers, timeout=10)
            assert r.status_code == 204
            r = requests.delete(f"{API}/servicos/{sid}/insumos/{iid}", headers=headers, timeout=10)
            assert r.status_code == 404
        finally:
            requests.delete(f"{API}/insumos/{iid}", headers=headers)
            requests.delete(f"{API}/servicos/{sid}", headers=headers)

    def test_delete_servico_removes_vinculos(self, headers):
        # criar serv + insumo + vincular
        sid = requests.post(f"{API}/servicos/", headers=headers,
                            json={"nome": "TEST_ServDelVinc", "duracao_minutos": 15, "valor": 5.0}, timeout=10).json()["id"]
        iid = requests.post(f"{API}/insumos/", headers=headers,
                            json={"nome": "TEST_InsDelVinc", "unidade": "un",
                                  "quantidade_atual": 3, "quantidade_minima_alerta": 1, "custo": 1.0}, timeout=10).json()["id"]
        requests.post(f"{API}/servicos/{sid}/insumos", headers=headers,
                      json={"insumo_id": iid, "quantidade_utilizada": 1}, timeout=10)
        # apagar servico -> vinculos deletados
        r = requests.delete(f"{API}/servicos/{sid}", headers=headers, timeout=10)
        assert r.status_code == 204
        # tentar listar -> 404
        r = requests.get(f"{API}/servicos/{sid}/insumos", headers=headers, timeout=10)
        assert r.status_code == 404
        # cleanup
        requests.delete(f"{API}/insumos/{iid}", headers=headers)


# ---------------- INSUMOS FLOAT + DEDUÇÃO ----------------

class TestInsumosFloat:
    def test_insumo_aceita_float(self, headers):
        p = {"nome": "TEST_Float", "unidade": "un", "quantidade_atual": 24.5,
             "quantidade_minima_alerta": 2.5, "custo": 3.75}
        r = requests.post(f"{API}/insumos/", headers=headers, json=p, timeout=10)
        assert r.status_code == 201, r.text
        iid = r.json()["id"]
        assert r.json()["quantidade_atual"] == 24.5
        r2 = requests.put(f"{API}/insumos/{iid}", headers=headers, json={"quantidade_atual": 30.25}, timeout=10)
        assert r2.status_code == 200 and r2.json()["quantidade_atual"] == 30.25
        requests.delete(f"{API}/insumos/{iid}", headers=headers)


class TestDeducaoEstoque:
    def test_concluir_deduz_e_alerta(self, headers):
        # criar servico + insumo com estoque=1, min=1
        sid = requests.post(f"{API}/servicos/", headers=headers,
                            json={"nome": "TEST_ServCon", "duracao_minutos": 30, "valor": 10.0}, timeout=10).json()["id"]
        iid = requests.post(f"{API}/insumos/", headers=headers,
                            json={"nome": "TEST_InsCon", "unidade": "un",
                                  "quantidade_atual": 2, "quantidade_minima_alerta": 1, "custo": 1.0}, timeout=10).json()["id"]
        requests.post(f"{API}/servicos/{sid}/insumos", headers=headers,
                      json={"insumo_id": iid, "quantidade_utilizada": 1}, timeout=10)
        # profissional
        profs = requests.get(f"{API}/profissionais/", headers=headers).json()
        pid = profs[0]["id"]
        # agendamento amanhã em horário livre
        start = _amanha_utc(21)  # UTC 21:00
        payload = {"servico_id": sid, "profissional_id": pid,
                   "cliente_nome": "TEST_Concl", "cliente_telefone": "11988887777",
                   "data_hora_inicio": start.isoformat().replace("+00:00", "Z")}
        r = requests.post(f"{API}/agendamentos/", headers=headers, json=payload, timeout=10)
        assert r.status_code == 201, r.text
        aid = r.json()["id"]
        try:
            # concluir
            r = requests.patch(f"{API}/agendamentos/{aid}/concluir", headers=headers, timeout=10)
            assert r.status_code == 200, r.text
            d = r.json()
            assert d["status"] == "concluido"
            assert any("TEST_InsCon" in a for a in d.get("alertas_estoque", [])), d.get("alertas_estoque")
            # verificar redução
            ins = requests.get(f"{API}/insumos/{iid}", headers=headers).json()
            assert ins["quantidade_atual"] == 1

            # concluir novamente NÃO deduz
            r2 = requests.patch(f"{API}/agendamentos/{aid}/concluir", headers=headers, timeout=10)
            assert r2.status_code == 200
            assert r2.json().get("alertas_estoque") == []
            ins2 = requests.get(f"{API}/insumos/{iid}", headers=headers).json()
            assert ins2["quantidade_atual"] == 1
        finally:
            requests.delete(f"{API}/agendamentos/{aid}", headers=headers)
            requests.delete(f"{API}/insumos/{iid}", headers=headers)
            requests.delete(f"{API}/servicos/{sid}", headers=headers)

    def test_concluir_sem_estoque_409(self, headers):
        sid = requests.post(f"{API}/servicos/", headers=headers,
                            json={"nome": "TEST_ServInsuf", "duracao_minutos": 30, "valor": 10.0}, timeout=10).json()["id"]
        iid = requests.post(f"{API}/insumos/", headers=headers,
                            json={"nome": "TEST_InsInsuf", "unidade": "un",
                                  "quantidade_atual": 0, "quantidade_minima_alerta": 1, "custo": 1.0}, timeout=10).json()["id"]
        requests.post(f"{API}/servicos/{sid}/insumos", headers=headers,
                      json={"insumo_id": iid, "quantidade_utilizada": 1}, timeout=10)
        profs = requests.get(f"{API}/profissionais/", headers=headers).json()
        pid = profs[0]["id"]
        start = _amanha_utc(22)
        payload = {"servico_id": sid, "profissional_id": pid,
                   "cliente_nome": "TEST_Insuf", "cliente_telefone": "11988886666",
                   "data_hora_inicio": start.isoformat().replace("+00:00", "Z")}
        aid = requests.post(f"{API}/agendamentos/", headers=headers, json=payload, timeout=10).json()["id"]
        try:
            r = requests.patch(f"{API}/agendamentos/{aid}/concluir", headers=headers, timeout=10)
            assert r.status_code == 409, r.text
        finally:
            requests.delete(f"{API}/agendamentos/{aid}", headers=headers)
            requests.delete(f"{API}/insumos/{iid}", headers=headers)
            requests.delete(f"{API}/servicos/{sid}", headers=headers)


# ---------------- ESTOQUE ALERTAS ----------------

class TestEstoqueAlertas:
    def test_alertas_types(self, headers):
        r = requests.get(f"{API}/estoque/alertas", headers=headers, timeout=10)
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        tipos = {a.get("tipo") for a in data if isinstance(a, dict)}
        # Deve pelo menos ter estrutura de tipo
        assert tipos.issubset({"minimo", "demanda"}) or tipos == set()

===== FILE: frontend/.env.example =====
REACT_APP_BACKEND_URL=http://localhost:8001

===== FILE: frontend/.gitignore =====
# See https://help.github.com/articles/ignoring-files/ for more about ignoring files.

# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# production
/build

# misc
.DS_Store
.env.local
.env.development.local
.env.test.local
.env.production.local

npm-debug.log*
yarn-debug.log*
yarn-error.log*

===== FILE: frontend/components.json =====
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": false,
  "tsx": false,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "src/index.css",
    "baseColor": "neutral",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
===== FILE: frontend/craco.config.js =====
// craco.config.js
const path = require("path");
require("dotenv").config();

// Check if we're in development/preview mode (not production build)
// Craco sets NODE_ENV=development for start, NODE_ENV=production for build
const isDevServer = process.env.NODE_ENV !== "production";

// Environment variable overrides
const config = {
  enableHealthCheck: process.env.ENABLE_HEALTH_CHECK === "true",
};

function makeDevServerV5Compatible(devServerConfig) {
  const {
    https,
    onAfterSetupMiddleware,
    onBeforeSetupMiddleware,
    onListening,
    setupMiddlewares,
    ...compatibleConfig
  } = devServerConfig;

  compatibleConfig.server =
    typeof https === "object"
      ? { type: "https", options: https }
      : https
        ? "https"
        : "http";
  compatibleConfig.headers = {
    ...compatibleConfig.headers,
    "Cross-Origin-Resource-Policy": "same-origin",
  };

  if (onBeforeSetupMiddleware || setupMiddlewares) {
    compatibleConfig.setupMiddlewares = (middlewares, devServer) => {
      if (onBeforeSetupMiddleware) {
        onBeforeSetupMiddleware(devServer);
      }

      return setupMiddlewares
        ? setupMiddlewares(middlewares, devServer)
        : middlewares;
    };
  }

  compatibleConfig.onListening = (devServer) => {
    devServer.close ??= (callback) => devServer.stopCallback(callback);

    if (onListening) {
      onListening(devServer);
    }
    if (onAfterSetupMiddleware) {
      onAfterSetupMiddleware(devServer);
    }
  };

  return compatibleConfig;
}

// Conditionally load health check modules only if enabled
let WebpackHealthPlugin;
let setupHealthEndpoints;
let healthPluginInstance;

if (config.enableHealthCheck) {
  WebpackHealthPlugin = require("./plugins/health-check/webpack-health-plugin");
  setupHealthEndpoints = require("./plugins/health-check/health-endpoints");
  healthPluginInstance = new WebpackHealthPlugin();
}

// Branded error overlay + preview health probe, dev server only. Fails open: a broken
// overlay must degrade to "no overlay", never to "no dev server".
let emergentOverlay;
if (isDevServer && process.env.DISABLE_EMERGENT_OVERLAY !== "true") {
  try {
    emergentOverlay = require("@emergentbase/overlay/craco").emergentOverlayCraco({
      root: __dirname,
    });
    // A wrong shape would otherwise TypeError at dev-server config time, past this catch.
    if (
      typeof emergentOverlay.devServer !== "function" ||
      typeof emergentOverlay.attach !== "function" ||
      typeof emergentOverlay.webpackPlugin?.apply !== "function"
    ) {
      throw new Error("unexpected adapter shape");
    }
  } catch (err) {
    emergentOverlay = undefined;
    console.warn(
      "[emergent-overlay] not loaded — overlay disabled:",
      err instanceof Error ? err.message : err,
    );
  }
}

let webpackConfig = {
  eslint: {
    configure: {
      extends: ["plugin:react-hooks/recommended"],
      rules: {
        "react-hooks/rules-of-hooks": "error",
        "react-hooks/exhaustive-deps": "warn",
      },
    },
  },
  webpack: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
    configure: (webpackConfig) => {

      // Add ignored patterns to reduce watched directories
        webpackConfig.watchOptions = {
          ...webpackConfig.watchOptions,
          ignored: [
            '**/node_modules/**',
            '**/.git/**',
            '**/build/**',
            '**/dist/**',
            '**/coverage/**',
            '**/public/**',
        ],
      };

      // Add health check plugin to webpack if enabled
      if (config.enableHealthCheck && healthPluginInstance) {
        webpackConfig.plugins.push(healthPluginInstance);
      }

      // Overlay's HTML injection + compile-error capture; self-gates on mode !== development.
      if (emergentOverlay) {
        webpackConfig.plugins.push(emergentOverlay.webpackPlugin);
      }
      return webpackConfig;
    },
  },
};

webpackConfig.devServer = (devServerConfig) => {
  // Add health check endpoints if enabled
  if (config.enableHealthCheck && setupHealthEndpoints && healthPluginInstance) {
    const originalSetupMiddlewares = devServerConfig.setupMiddlewares;

    devServerConfig.setupMiddlewares = (middlewares, devServer) => {
      // Call original setup if exists
      if (originalSetupMiddlewares) {
        middlewares = originalSetupMiddlewares(middlewares, devServer);
      }

      // Setup health endpoints
      setupHealthEndpoints(devServer, healthPluginInstance);

      return middlewares;
    };
  }

  return devServerConfig;
};

// Wrap with visual edits (automatically adds babel plugin, dev server, and overlay in dev mode)
if (isDevServer) {
  try {
    const { withVisualEdits } = require("@emergentbase/visual-edits/craco");
    webpackConfig = withVisualEdits(webpackConfig);
  } catch (err) {
    if (err.code === 'MODULE_NOT_FOUND' && err.message.includes('@emergentbase/visual-edits/craco')) {
      console.warn(
        "[visual-edits] @emergentbase/visual-edits not installed — visual editing disabled."
      );
    } else {
      throw err;
    }
  }
}

// Overlay wraps last: visual-edits assigns setupMiddlewares instead of chaining onto it,
// so anything registered before it is dropped.
if (emergentOverlay) {
  const devServerBeforeOverlay = webpackConfig.devServer;

  // Fail open at each call site too: a throw inside the adapter costs the overlay, never
  // the dev server. Warns once, then this path stops calling it.
  let overlay = emergentOverlay;
  const overlayFailed = (site, err) => {
    overlay = undefined;
    console.warn(
      `[emergent-overlay] ${site} failed — overlay disabled:`,
      err instanceof Error ? err.message : err,
    );
  };

  webpackConfig.devServer = (devServerConfig) => {
    devServerConfig = devServerBeforeOverlay(devServerConfig);

    // Overlay owns runtime errors; webpack keeps compile errors.
    try {
      devServerConfig = overlay.devServer(devServerConfig);
    } catch (err) {
      overlayFailed("devServer config", err);
    }

    const previousSetupMiddlewares = devServerConfig.setupMiddlewares;

    devServerConfig.setupMiddlewares = (middlewares, devServer) => {
      // Registered ahead of the chain's own body parsers, which would consume the raw stream
      // the overlay reads. Adapter taking a pre-parsed req.body is the overlay-side fix.
      try {
        if (overlay) overlay.attach(devServer);
      } catch (err) {
        overlayFailed("attach", err);
      }

      if (previousSetupMiddlewares) {
        middlewares = previousSetupMiddlewares(middlewares, devServer);
      }

      return middlewares;
    };

    return devServerConfig;
  };
}

const configureDevServer = webpackConfig.devServer;
webpackConfig.devServer = (devServerConfig) =>
  makeDevServerV5Compatible(configureDevServer(devServerConfig));

module.exports = webpackConfig;

===== FILE: frontend/jsconfig.json =====
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"]
}
===== FILE: frontend/package.json =====
{
  "name": "frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "@hookform/resolvers": "5.0.1",
    "@radix-ui/react-accordion": "1.2.8",
    "@radix-ui/react-alert-dialog": "1.1.11",
    "@radix-ui/react-aspect-ratio": "1.1.4",
    "@radix-ui/react-avatar": "1.1.7",
    "@radix-ui/react-checkbox": "1.2.3",
    "@radix-ui/react-collapsible": "1.1.8",
    "@radix-ui/react-context-menu": "2.2.12",
    "@radix-ui/react-dialog": "1.1.11",
    "@radix-ui/react-dropdown-menu": "2.1.12",
    "@radix-ui/react-hover-card": "1.1.11",
    "@radix-ui/react-label": "2.1.4",
    "@radix-ui/react-menubar": "1.1.12",
    "@radix-ui/react-navigation-menu": "1.2.10",
    "@radix-ui/react-popover": "1.1.11",
    "@radix-ui/react-progress": "1.1.4",
    "@radix-ui/react-radio-group": "1.3.4",
    "@radix-ui/react-scroll-area": "1.2.6",
    "@radix-ui/react-select": "2.2.2",
    "@radix-ui/react-separator": "1.1.4",
    "@radix-ui/react-slider": "1.3.2",
    "@radix-ui/react-slot": "1.2.0",
    "@radix-ui/react-switch": "1.2.2",
    "@radix-ui/react-tabs": "1.1.9",
    "@radix-ui/react-toast": "1.2.11",
    "@radix-ui/react-toggle": "1.1.6",
    "@radix-ui/react-toggle-group": "1.1.7",
    "@radix-ui/react-tooltip": "1.2.4",
    "@tanstack/react-query": "5.56.2",
    "axios": "1.18.0",
    "class-variance-authority": "0.7.1",
    "clsx": "2.1.1",
    "cmdk": "1.1.1",
    "cra-template": "1.2.0",
    "date-fns": "4.1.0",
    "dayjs": "1.11.13",
    "embla-carousel-react": "8.6.0",
    "framer-motion": "11.18.0",
    "input-otp": "1.4.2",
    "lodash": "4.18.1",
    "lucide-react": "0.516.0",
    "next-themes": "0.4.6",
    "react": "19.0.0",
    "react-day-picker": "8.10.1",
    "react-dom": "19.0.0",
    "react-hook-form": "7.56.2",
    "react-resizable-panels": "3.0.1",
    "react-router-dom": "7.15.0",
    "react-scripts": "5.0.1",
    "recharts": "3.6.0",
    "sonner": "2.0.3",
    "swr": "2.3.8",
    "tailwind-merge": "3.2.0",
    "tailwindcss-animate": "1.0.7",
    "vaul": "1.1.2",
    "zod": "3.24.4"
  },
  "scripts": {
    "start": "craco start",
    "build": "craco build",
    "test": "craco test"
  },
  "browserslist": {
    "production": [
      ">0.2%",
      "not dead",
      "not op_mini all"
    ],
    "development": [
      "last 1 chrome version",
      "last 1 firefox version",
      "last 1 safari version"
    ]
  },
  "devDependencies": {
    "@babel/plugin-proposal-private-property-in-object": "7.21.11",
    "@craco/craco": "7.1.0",
    "@emergentbase/overlay": "https://assets.emergent.sh/npm/emergentbase-overlay-0.1.29.tgz",
    "@emergentbase/visual-edits": "https://assets.emergent.sh/npm/emergentbase-visual-edits-1.0.13.tgz",
    "@eslint/js": "9.23.0",
    "@types/lodash": "4.17.24",
    "autoprefixer": "10.4.20",
    "dotenv": "16.4.5",
    "eslint": "9.23.0",
    "eslint-plugin-import": "2.31.0",
    "eslint-plugin-jsx-a11y": "6.10.2",
    "eslint-plugin-react": "7.37.4",
    "eslint-plugin-react-hooks": "5.2.0",
    "globals": "15.15.0",
    "postcss": "8.5.10",
    "tailwindcss": "3.4.17"
  },
  "resolutions": {
    "react-router": "7.15.1",
    "node-forge": "1.4.0",
    "fast-uri": "3.1.2",
    "flatted": "3.4.2",
    "qs": "6.15.2",
    "diff": "4.0.4",
    "follow-redirects": "1.16.0",
    "path-to-regexp": "0.1.13",
    "rollup": "2.80.0",
    "underscore": "1.13.8",
    "@babel/plugin-transform-modules-systemjs": "7.29.4",
    "@eslint/plugin-kit": "0.3.4",
    "shell-quote": "1.9.0",
    "jsonpath": "1.3.0",
    "nth-check": "2.0.1",
    "serialize-javascript": "7.0.5",
    "uuid": "11.1.1",
    "@tootallnate/once": "2.0.1",
    "webpack-dev-server": "5.2.6",
    "resolve-url-loader": "5.0.0",
    "**/resolve-url-loader/postcss": "8.5.10",
    "**/axios/form-data": "4.0.6",
    "**/jsdom/form-data": "3.0.5",
    "**/postcss-svgo/svgo": "2.8.1",
    "**/webpack-dev-server/ws": "8.21.0",
    "**/postcss-load-config/yaml": "2.8.3",
    "**/cosmiconfig/yaml": "1.10.3",
    "**/cssnano/yaml": "1.10.3",
    "**/eslint/js-yaml": "4.3.0",
    "**/@eslint/eslintrc/js-yaml": "4.3.0",
    "**/svgo/js-yaml": "3.15.0",
    "**/@istanbuljs/load-nyc-config/js-yaml": "3.15.0",
    "**/css-loader/postcss": "8.5.10",
    "**/css-minimizer-webpack-plugin/postcss": "8.5.10",
    "**/react-scripts/postcss": "8.5.10",
    "**/filelist/minimatch": "5.1.8",
    "**/anymatch/picomatch": "2.3.2",
    "**/micromatch/picomatch": "2.3.2",
    "**/readdirp/picomatch": "2.3.2",
    "**/jest-util/picomatch": "2.3.2",
    "**/tinyglobby/picomatch": "4.0.4",
    "http-proxy-middleware": "2.0.10"
  },
  "packageManager": "yarn@1.22.22+sha512.a6b2f7906b721bba3d67d4aff083df04dad64c399707841b7acf00f6b133b7ac24255f2652fa22ae3534329dc6180534e98d17432037ff6fd140556e2bb3137e"
}

===== FILE: frontend/plugins/health-check/health-endpoints.js =====
// health-endpoints.js
// API endpoints for health checks and monitoring

const os = require('os');

const SERVER_START_TIME = Date.now();

/**
 * Setup health check endpoints on the dev server
 * @param {Object} devServer - Webpack dev server instance
 * @param {Object} healthPlugin - Instance of WebpackHealthPlugin
 */
function setupHealthEndpoints(devServer, healthPlugin) {
  if (!devServer || !devServer.app) {
    console.warn('[Health Check] Dev server not available, skipping health endpoints');
    return;
  }

  if (!healthPlugin) {
    console.warn('[Health Check] Health plugin not provided, skipping health endpoints');
    return;
  }

  console.log('[Health Check] Setting up health endpoints...');

  // ====================================================================
  // GET /health - Detailed health status (JSON)
  // ====================================================================
  devServer.app.get("/health", (req, res) => {
    const webpackStatus = healthPlugin.getStatus();
    const uptime = Date.now() - SERVER_START_TIME;
    const memUsage = process.memoryUsage();

    res.json({
      status: webpackStatus.isHealthy ? 'healthy' : 'unhealthy',
      timestamp: new Date().toISOString(),
      uptime: {
        seconds: Math.floor(uptime / 1000),
        formatted: formatDuration(uptime),
      },
      webpack: {
        state: webpackStatus.state,
        isHealthy: webpackStatus.isHealthy,
        hasCompiled: webpackStatus.hasCompiled,
        errors: webpackStatus.errorCount,
        warnings: webpackStatus.warningCount,
        lastCompileTime: webpackStatus.lastCompileTime
          ? new Date(webpackStatus.lastCompileTime).toISOString()
          : null,
        lastSuccessTime: webpackStatus.lastSuccessTime
          ? new Date(webpackStatus.lastSuccessTime).toISOString()
          : null,
        compileDuration: webpackStatus.compileDuration
          ? `${webpackStatus.compileDuration}ms`
          : null,
        totalCompiles: webpackStatus.totalCompiles,
        firstCompileTime: webpackStatus.firstCompileTime
          ? new Date(webpackStatus.firstCompileTime).toISOString()
          : null,
      },
      server: {
        nodeVersion: process.version,
        platform: os.platform(),
        arch: os.arch(),
        cpus: os.cpus().length,
        memory: {
          heapUsed: formatBytes(memUsage.heapUsed),
          heapTotal: formatBytes(memUsage.heapTotal),
          rss: formatBytes(memUsage.rss),
          external: formatBytes(memUsage.external),
        },
        systemMemory: {
          total: formatBytes(os.totalmem()),
          free: formatBytes(os.freemem()),
          used: formatBytes(os.totalmem() - os.freemem()),
        },
      },
      environment: process.env.NODE_ENV || 'development',
    });
  });

  // ====================================================================
  // GET /health/simple - Simple text response (OK/COMPILING/ERROR)
  // ====================================================================
  devServer.app.get("/health/simple", (req, res) => {
    const webpackStatus = healthPlugin.getSimpleStatus();

    if (webpackStatus.state === 'success') {
      res.status(200).send('OK');
    } else if (webpackStatus.state === 'compiling') {
      res.status(200).send('COMPILING');
    } else if (webpackStatus.state === 'idle') {
      res.status(200).send('IDLE');
    } else {
      res.status(503).send('ERROR');
    }
  });

  // ====================================================================
  // GET /health/ready - Readiness check (Kubernetes/load balancer)
  // ====================================================================
  devServer.app.get("/health/ready", (req, res) => {
    const webpackStatus = healthPlugin.getSimpleStatus();

    if (webpackStatus.state === 'success') {
      res.status(200).json({
        ready: true,
        state: webpackStatus.state,
      });
    } else {
      res.status(503).json({
        ready: false,
        state: webpackStatus.state,
        reason: webpackStatus.state === 'compiling'
          ? 'Compilation in progress'
          : 'Compilation failed',
      });
    }
  });

  // ====================================================================
  // GET /health/live - Liveness check (Kubernetes)
  // ====================================================================
  devServer.app.get("/health/live", (req, res) => {
    res.status(200).json({
      alive: true,
      timestamp: new Date().toISOString(),
    });
  });

  // ====================================================================
  // GET /health/errors - Get current errors and warnings
  // ====================================================================
  devServer.app.get("/health/errors", (req, res) => {
    const webpackStatus = healthPlugin.getStatus();

    res.json({
      errorCount: webpackStatus.errorCount,
      warningCount: webpackStatus.warningCount,
      errors: webpackStatus.errors,
      warnings: webpackStatus.warnings,
      state: webpackStatus.state,
    });
  });

  // ====================================================================
  // GET /health/stats - Compilation statistics
  // ====================================================================
  devServer.app.get("/health/stats", (req, res) => {
    const webpackStatus = healthPlugin.getStatus();
    const uptime = Date.now() - SERVER_START_TIME;

    res.json({
      totalCompiles: webpackStatus.totalCompiles,
      averageCompileTime: webpackStatus.totalCompiles > 0
        ? `${Math.round(uptime / webpackStatus.totalCompiles)}ms`
        : null,
      lastCompileDuration: webpackStatus.compileDuration
        ? `${webpackStatus.compileDuration}ms`
        : null,
      firstCompileTime: webpackStatus.firstCompileTime
        ? new Date(webpackStatus.firstCompileTime).toISOString()
        : null,
      serverUptime: formatDuration(uptime),
    });
  });

  console.log('[Health Check] ✓ Health endpoints ready:');
  console.log('  • GET /health         - Detailed status');
  console.log('  • GET /health/simple  - Simple OK/ERROR');
  console.log('  • GET /health/ready   - Readiness check');
  console.log('  • GET /health/live    - Liveness check');
  console.log('  • GET /health/errors  - Error details');
  console.log('  • GET /health/stats   - Statistics');
}

// ====================================================================
// Helper Functions
// ====================================================================

/**
 * Format bytes to human-readable string
 * @param {number} bytes
 * @returns {string}
 */
function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}

/**
 * Format duration to human-readable string
 * @param {number} ms - Duration in milliseconds
 * @returns {string}
 */
function formatDuration(ms) {
  const seconds = Math.floor(ms / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);

  if (hours > 0) {
    return `${hours}h ${minutes % 60}m ${seconds % 60}s`;
  } else if (minutes > 0) {
    return `${minutes}m ${seconds % 60}s`;
  } else {
    return `${seconds}s`;
  }
}

module.exports = setupHealthEndpoints;

===== FILE: frontend/plugins/health-check/webpack-health-plugin.js =====
// webpack-health-plugin.js
// Webpack plugin that tracks compilation state and health metrics

class WebpackHealthPlugin {
  constructor() {
    this.status = {
      state: 'idle',           // idle, compiling, success, failed
      errors: [],
      warnings: [],
      lastCompileTime: null,
      lastSuccessTime: null,
      compileDuration: 0,
      totalCompiles: 0,
      firstCompileTime: null,
    };
  }

  apply(compiler) {
    const pluginName = 'WebpackHealthPlugin';

    // Hook: Compilation started
    compiler.hooks.compile.tap(pluginName, () => {
      const now = Date.now();
      this.status.state = 'compiling';
      this.status.lastCompileTime = now;

      if (!this.status.firstCompileTime) {
        this.status.firstCompileTime = now;
      }
    });

    // Hook: Compilation completed
    compiler.hooks.done.tap(pluginName, (stats) => {
      const info = stats.toJson({
        all: false,
        errors: true,
        warnings: true,
      });

      this.status.totalCompiles++;
      this.status.compileDuration = Date.now() - this.status.lastCompileTime;

      if (stats.hasErrors()) {
        this.status.state = 'failed';
        this.status.errors = info.errors.map(err => ({
          message: err.message || String(err),
          stack: err.stack,
          moduleName: err.moduleName,
          loc: err.loc,
        }));
      } else {
        this.status.state = 'success';
        this.status.lastSuccessTime = Date.now();
        this.status.errors = [];
      }

      if (stats.hasWarnings()) {
        this.status.warnings = info.warnings.map(warn => ({
          message: warn.message || String(warn),
          moduleName: warn.moduleName,
          loc: warn.loc,
        }));
      } else {
        this.status.warnings = [];
      }
    });

    // Hook: Compilation failed
    compiler.hooks.failed.tap(pluginName, (error) => {
      this.status.state = 'failed';
      this.status.errors = [{
        message: error.message,
        stack: error.stack,
      }];
      this.status.compileDuration = Date.now() - this.status.lastCompileTime;
    });

    // Hook: Invalid (file changed, recompiling)
    compiler.hooks.invalid.tap(pluginName, () => {
      this.status.state = 'compiling';
    });
  }

  getStatus() {
    return {
      ...this.status,
      // Add computed fields
      isHealthy: this.status.state === 'success',
      errorCount: this.status.errors.length,
      warningCount: this.status.warnings.length,
      hasCompiled: this.status.totalCompiles > 0,
    };
  }

  // Get simplified status for quick checks
  getSimpleStatus() {
    return {
      state: this.status.state,
      isHealthy: this.status.state === 'success',
      errorCount: this.status.errors.length,
      warningCount: this.status.warnings.length,
    };
  }

  // Reset statistics (useful for testing)
  reset() {
    this.status = {
      state: 'idle',
      errors: [],
      warnings: [],
      lastCompileTime: null,
      lastSuccessTime: null,
      compileDuration: 0,
      totalCompiles: 0,
      firstCompileTime: null,
    };
  }
}

module.exports = WebpackHealthPlugin;

===== FILE: frontend/postcss.config.js =====
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}

===== FILE: frontend/public/index.html =====
<!doctype html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content="#000000" />
        <meta name="description" content="A product of emergent.sh" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@600&display=swap" rel="stylesheet" />
        <!--
        manifest.json provides metadata used when your web app is installed on a
        user's mobile device or desktop. See https://developers.google.com/web/fundamentals/web-app-manifest/
        -->
        <!--
        Notice the use of %PUBLIC_URL% in the tags above.
        It will be replaced with the URL of the `public` folder during the build.
        Only files inside the `public` folder can be referenced from the HTML.

        Unlike "/favicon.ico" or "favicon.ico", "%PUBLIC_URL%/favicon.ico" will
        work correctly both with client-side routing and a non-root public URL.
        Learn how to configure a non-root public URL by running `npm run build`.
        -->
        <title>Emergent | Fullstack App</title>
        <script>window.addEventListener("error",function(e){if(e.error instanceof DOMException&&e.error.name==="DataCloneError"&&e.message&&e.message.includes("PerformanceServerTiming")){e.stopImmediatePropagation();e.preventDefault()}},true);</script>
        <script src="https://assets.emergent.sh/scripts/emergent-main.js"></script>
    </head>
    <body>
        <noscript>You need to enable JavaScript to run this app.</noscript>
        <div id="root"></div>
        <!--
      This HTML file is a template.
      If you open it directly in the browser, you will see an empty page.

      You can add webfonts, meta tags, or analytics to this file.
      The build step will place the bundled scripts into the <body> tag.

      To begin the development, run `npm start` or `yarn start`.
      To create a production bundle, use `npm run build` or `yarn build`.
    -->
        <script>
            !(function (t, e) {
                var o, n, p, r;
                e.__SV ||
                    ((window.posthog = e),
                    (e._i = []),
                    (e.init = function (i, s, a) {
                        function g(t, e) {
                            var o = e.split(".");
                            2 == o.length && ((t = t[o[0]]), (e = o[1])),
                                (t[e] = function () {
                                    t.push(
                                        [e].concat(
                                            Array.prototype.slice.call(
                                                arguments,
                                                0,
                                            ),
                                        ),
                                    );
                                });
                        }
                        ((p = t.createElement("script")).type =
                            "text/javascript"),
                            (p.crossOrigin = "anonymous"),
                            (p.async = !0),
                            (p.src =
                                s.api_host.replace(
                                    ".i.posthog.com",
                                    "-assets.i.posthog.com",
                                ) + "/static/array.js"),
                            (r =
                                t.getElementsByTagName(
                                    "script",
                                )[0]).parentNode.insertBefore(p, r);
                        var u = e;
                        for (
                            void 0 !== a ? (u = e[a] = []) : (a = "posthog"),
                                u.people = u.people || [],
                                u.toString = function (t) {
                                    var e = "posthog";
                                    return (
                                        "posthog" !== a && (e += "." + a),
                                        t || (e += " (stub)"),
                                        e
                                    );
                                },
                                u.people.toString = function () {
                                    return u.toString(1) + ".people (stub)";
                                },
                                o =
                                    "init me ws ys ps bs capture je Di ks register register_once register_for_session unregister unregister_for_session Ps getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSurveysLoaded onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey canRenderSurveyAsync identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty Es $s createPersonProfile Is opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing Ss debug xs getPageViewId captureTraceFeedback captureTraceMetric".split(
                                        " ",
                                    ),
                                n = 0;
                            n < o.length;
                            n++
                        )
                            g(u, o[n]);
                        e._i.push([i, s, a]);
                    }),
                    (e.__SV = 1));
            })(document, window.posthog || []);
            posthog.init("phc_DbsPb39SRc8z3EiQ6Dhj6ikv4H4rTKcht9d4sZSesceP", {
                api_host: "https://ap.emergent.sh",
                person_profiles: "identified_only", // or 'always' to create profiles for anonymous users as well,
                session_recording: {
                    recordCrossOriginIframes: true,
                    capturePerformance: false,
                },
            });
        </script>
    </body>
</html>

===== FILE: frontend/src/App.css =====
/* App-level styles are in index.css */
.App { min-height: 100vh; }

===== FILE: frontend/src/App.js =====
import { BrowserRouter, Navigate, Route, Routes, useLocation } from "react-router-dom";
import "@/App.css";
import { AuthProvider, useAuth } from "@/context/AuthContext";
import { ToastProvider } from "@/context/ToastContext";
import Landing from "@/pages/Landing";
import AppShell from "@/components/AppShell";
import AuthCallback from "@/components/AuthCallback";
import Agenda from "@/pages/Agenda";
import Perfil from "@/pages/Perfil";
import Atendimento from "@/pages/Atendimento";
import Estoque from "@/pages/Estoque";
import Financeiro from "@/pages/Financeiro";
import Configuracoes from "@/pages/Configuracoes";

function Protected({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading">Carregando…</div>;
  if (!user) return <Navigate to="/" replace />;
  return children;
}

function PublicOnly({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading">Carregando…</div>;
  if (user) return <Navigate to="/app/atendimento" replace />;
  return children;
}

function AppRouter() {
  const location = useLocation();
  if (location.hash?.includes("session_id=")) return <AuthCallback />;
  return (
    <Routes>
      <Route path="/" element={<PublicOnly><Landing /></PublicOnly>} />
      <Route path="/app" element={<Protected><AppShell /></Protected>}>
        <Route index element={<Navigate to="/app/atendimento" replace />} />
        <Route path="agenda" element={<Agenda />} />
        <Route path="perfil" element={<Perfil />} />
        <Route path="atendimento" element={<Atendimento />} />
        <Route path="estoque" element={<Estoque />} />
        <Route path="financeiro" element={<Financeiro />} />
        <Route path="configuracoes" element={<Configuracoes />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <ToastProvider>
      <AuthProvider>
        <BrowserRouter>
          <AppRouter />
        </BrowserRouter>
      </AuthProvider>
    </ToastProvider>
  );
}

===== FILE: frontend/src/components/AppShell.jsx =====
import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { Calendar, User, MessageCircle, Package, DollarSign, Settings, Shield, HelpCircle, Search } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

const NAV = [
  { to: "/app/agenda", label: "Agenda", icon: Calendar },
  { to: "/app/perfil", label: "Perfil", icon: User },
  { to: "/app/atendimento", label: "Atendimento", icon: MessageCircle },
  { to: "/app/estoque", label: "Estoque", icon: Package },
  { to: "/app/financeiro", label: "Financeiro", icon: DollarSign },
  { to: "/app/configuracoes", label: "Configurações", icon: Settings },
];

const CRUMBS = {
  "/app/agenda": ["Visão geral", "Agenda"],
  "/app/perfil": ["Visão geral", "Perfil"],
  "/app/atendimento": ["Visão geral", "Atendimento"],
  "/app/estoque": ["Visão geral", "Estoque"],
  "/app/financeiro": ["Visão geral", "Financeiro"],
  "/app/configuracoes": ["Visão geral", "Configurações"],
};

export default function AppShell() {
  const { user, logout } = useAuth();
  const loc = useLocation();
  const nav = useNavigate();
  const crumbs = CRUMBS[loc.pathname] || ["Visão geral", "Agenda"];
  const currentLabel = crumbs[1];
  const initials = (user?.nome || "AE").split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase();

  const doLogout = async () => { await logout(); nav("/"); };

  return (
    <div className="app-shell">
      <aside className="sidebar" data-testid="app-sidebar">
        <div className="sidebar-brand">
          <span className="mono">E</span>
          <div>
            <strong>ELO</strong>
            <small>beauty care</small>
          </div>
        </div>

        <div>
          <span className="sidebar-eyebrow">Espaço de gestão</span>
          <nav className="sidebar-nav">
            {NAV.map((n) => (
              <NavLink key={n.to} to={n.to} data-testid={`nav-${n.label.toLowerCase()}`}
                className={({ isActive }) => `sidebar-item ${isActive ? "active" : ""}`}>
                <n.icon size={18} />
                <span>{n.label}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="sidebar-bottom">
          <button className="sidebar-item" data-testid="nav-account-security" onClick={doLogout}>
            <Shield size={18} />
            <span>Conta e segurança</span>
          </button>
        </div>
      </aside>

      <div className="main">
        <div className="topbar">
          <div className="topbar-crumbs">
            <span>{crumbs[0]}</span>
            <span className="sep">›</span>
            <span className="active">{crumbs[1]}</span>
          </div>
          <div className="topbar-search">
            <Search size={16} />
            <input placeholder={`Buscar em ${currentLabel}`} data-testid="topbar-search" />
            <span className="topbar-kbd">⌘K</span>
          </div>
          <button className="topbar-icon" data-testid="topbar-help" aria-label="Ajuda">
            <HelpCircle size={18} />
          </button>
          <div className="topbar-user">
            <div className="topbar-avatar" data-testid="topbar-avatar">{initials}</div>
            <div>
              <strong>{user?.nome || "Admin ELO"}</strong>
              <small>{user?.business || "ELO Beauty Care"}</small>
            </div>
          </div>
        </div>

        <div className="content">
          <Outlet />
        </div>
      </div>
    </div>
  );
}

===== FILE: frontend/src/components/AuthCallback.jsx =====
import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { useToast } from "@/context/ToastContext";

export default function AuthCallback() {
  const { processSession } = useAuth();
  const nav = useNavigate();
  const location = useLocation();
  const toast = useToast();
  const processed = useRef(false);

  useEffect(() => {
    if (processed.current) return;
    processed.current = true;
    const sessionId = new URLSearchParams(location.hash.replace(/^#/, "")).get("session_id");
    (async () => {
      try {
        await processSession(sessionId);
        window.history.replaceState(null, "", location.pathname);
        toast("Bem-vinda de volta", "success");
        nav("/app/atendimento", { replace: true });
      } catch {
        window.history.replaceState(null, "", "/");
        toast("Não foi possível entrar com o Google", "error");
        nav("/", { replace: true });
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return <div className="loading" data-testid="auth-callback">Conectando sua conta Google…</div>;
}

===== FILE: frontend/src/components/LembretesVespera.jsx =====
import { useEffect, useState } from "react";
import { Sparkles, Send, MessageCircle, CheckCircle2, AlertTriangle, RefreshCw } from "lucide-react";
import { api, streamSSE } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

const hora = (iso) => new Date(iso).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
const waLink = (item) => `https://wa.me/${(item.telefone_e164 || "").replace("+", "")}?text=${encodeURIComponent(item.lembrete?.mensagem || "")}`;
const initials = (n) => (n || "C").split(" ").map((p) => p[0]).slice(0, 2).join("").toUpperCase();

function LinhaLembrete({ item, config, onChange }) {
  const toast = useToast();
  const [texto, setTexto] = useState(item.lembrete?.mensagem || "");
  const [enviando, setEnviando] = useState(false);
  useEffect(() => { setTexto(item.lembrete?.mensagem || ""); }, [item.lembrete?.mensagem]);

  const enviado = !!item.lembrete?.enviado_em;

  const salvar = async () => {
    const t = texto.trim();
    if (!t || t === item.lembrete?.mensagem) return;
    try { const { data } = await api.put(`/lembretes/vespera/${item.id}`, { mensagem: t }); onChange(data); }
    catch { toast("Erro ao salvar mensagem", "error"); }
  };

  const enviar = async (canal) => {
    if (!texto.trim()) { toast("Gere ou escreva a mensagem primeiro", "error"); return; }
    setEnviando(true);
    try {
      const { data } = await api.post(`/lembretes/vespera/${item.id}/enviar`, { canal, mensagem: texto.trim() });
      if (data.item) onChange(data.item);
      if (data.ok) toast(canal === "twilio" ? `Enviado para ${item.cliente_nome || "cliente"}` : "Marcado como enviado", "success");
      else toast(data.detalhe || "Falha no envio", "error");
    } catch (ex) { toast(ex.response?.data?.detail || "Falha no envio", "error"); }
    finally { setEnviando(false); }
  };

  return (
    <div className={`vespera-row ${enviado ? "sent" : ""}`} data-testid={`vespera-${item.id}`}>
      <div className="vespera-who">
        <div className={`avatar-sm ${enviado ? "green" : ""}`}>{initials(item.cliente_nome)}</div>
        <div className="body">
          <strong>{item.cliente_nome || "Cliente"}</strong>
          <span className="sub">{hora(item.data_hora_inicio)} · {item.servico_nome} · com {item.profissional_nome}</span>
          <span className="sub mono-tel">{item.telefone_e164 || item.cliente_telefone || "sem telefone"}</span>
        </div>
        {enviado ? (
          <span className="badge green" data-testid={`vespera-status-${item.id}`}><CheckCircle2 size={11} /> enviado {hora(item.lembrete.enviado_em)}</span>
        ) : item.lembrete?.erro ? (
          <span className="badge red" title={item.lembrete.erro} data-testid={`vespera-status-${item.id}`}><AlertTriangle size={11} /> falhou</span>
        ) : texto ? (
          <span className="badge gold" data-testid={`vespera-status-${item.id}`}>pronta</span>
        ) : (
          <span className="badge rose" data-testid={`vespera-status-${item.id}`}>pendente</span>
        )}
      </div>
      <textarea
        className="vespera-text"
        rows={2}
        placeholder="Clique em “Gerar todas com IA” ou escreva a mensagem aqui…"
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        onBlur={salvar}
        data-testid={`vespera-msg-${item.id}`}
      />
      <div className="vespera-actions">
        <a
          className={`btn-inline btn-wa small ${!texto || !item.telefone_e164 ? "disabled" : ""}`}
          href={texto && item.telefone_e164 ? waLink({ ...item, lembrete: { mensagem: texto } }) : undefined}
          target="_blank" rel="noreferrer"
          onClick={(e) => { if (!texto || !item.telefone_e164) { e.preventDefault(); return; } if (!enviado) enviar("whatsapp_link"); }}
          data-testid={`vespera-wa-${item.id}`}
        >
          <MessageCircle size={14} /> WhatsApp
        </a>
        <button
          type="button"
          className="btn-inline small primary"
          disabled={!config.twilio_configurado || enviando || enviado || !texto}
          title={config.twilio_configurado ? "Enviar automaticamente via Twilio" : "Configure o Twilio para envio automático"}
          onClick={() => enviar("twilio")}
          data-testid={`vespera-send-${item.id}`}
        >
          <Send size={14} /> {enviando ? "Enviando…" : "Enviar"}
        </button>
      </div>
    </div>
  );
}

export default function LembretesVespera() {
  const toast = useToast();
  const [itens, setItens] = useState([]);
  const [config, setConfig] = useState({ twilio_configurado: false, sandbox: false });
  const [gerando, setGerando] = useState(false);
  const [enviandoTodos, setEnviandoTodos] = useState(false);
  const [carregado, setCarregado] = useState(false);

  const load = async () => {
    try {
      const [{ data: lista }, { data: cfg }] = await Promise.all([api.get("/lembretes/vespera"), api.get("/lembretes/config")]);
      setItens(lista); setConfig(cfg);
    } catch { toast("Erro ao carregar lembretes de amanhã", "error"); }
    finally { setCarregado(true); }
  };
  useEffect(() => { load(); /* eslint-disable-next-line */ }, []);

  const patch = (novo) => setItens((v) => v.map((i) => (i.id === novo.id ? novo : i)));

  const gerarTodas = async () => {
    if (!itens.length) return;
    setGerando(true);
    let falhas = 0;
    try {
      await streamSSE("/ai/lembretes-vespera", {}, {
        onMeta: (ev) => {
          if (ev.agendamento_id) {
            setItens((v) => v.map((i) => i.id === ev.agendamento_id
              ? { ...i, lembrete: { ...(i.lembrete || {}), mensagem: ev.mensagem, gerado_em: new Date().toISOString() } }
              : i));
          }
          if (ev.falha) falhas += 1;
        },
      });
      toast(falhas ? `Geradas com ${falhas} falha(s)` : "Mensagens geradas pela IA", falhas ? "warning" : "success");
    } catch (ex) { toast(ex.message, "error"); }
    finally { setGerando(false); }
  };

  const enviarTodas = async () => {
    setEnviandoTodos(true);
    try {
      const { data } = await api.post("/lembretes/vespera/enviar-todos");
      data.forEach((r) => r.item && patch(r.item));
      const ok = data.filter((r) => r.ok).length;
      toast(`${ok}/${data.length} lembrete(s) enviados`, ok === data.length ? "success" : "warning");
    } catch (ex) { toast(ex.response?.data?.detail || "Falha no envio em lote", "error"); }
    finally { setEnviandoTodos(false); }
  };

  const pendentesComTexto = itens.filter((i) => i.lembrete?.mensagem && !i.lembrete?.enviado_em).length;
  const enviados = itens.filter((i) => i.lembrete?.enviado_em).length;

  return (
    <section className="card vespera-card" data-testid="card-lembretes-vespera">
      <div className="vespera-head">
        <div>
          <span className="card-eyebrow">Confirmação automática</span>
          <h3>Lembretes de amanhã</h3>
          <p className="desc">
            {carregado && itens.length === 0
              ? "Nenhum agendamento para amanhã."
              : `${itens.length} atendimento(s) amanhã · ${enviados} enviado(s). A IA escreve uma mensagem personalizada para cada cliente.`}
          </p>
        </div>
        <div className="vespera-cta">
          <button type="button" className="topbar-icon" title="Atualizar" onClick={load} data-testid="btn-vespera-refresh"><RefreshCw size={15} /></button>
          <button type="button" className="btn-ai lg" onClick={gerarTodas} disabled={gerando || !itens.length} data-testid="btn-gerar-todas-ia">
            <Sparkles size={14} /> {gerando ? "Escrevendo…" : "Gerar todas com IA"}
          </button>
          <button
            type="button"
            className="btn-inline primary"
            onClick={enviarTodas}
            disabled={!config.twilio_configurado || enviandoTodos || pendentesComTexto === 0}
            title={config.twilio_configurado ? "Envia via Twilio todas as mensagens prontas" : "Configure o Twilio para enviar em lote"}
            data-testid="btn-enviar-todas"
          >
            <Send size={14} /> {enviandoTodos ? "Enviando…" : `Enviar todas${pendentesComTexto ? ` (${pendentesComTexto})` : ""}`}
          </button>
        </div>
      </div>

      {!config.twilio_configurado && carregado && (
        <div className="vespera-note" data-testid="twilio-off-note">
          <AlertTriangle size={14} />
          <span>
            Envio automático desativado. Preencha <code>TWILIO_ACCOUNT_SID</code>, <code>TWILIO_AUTH_TOKEN</code> e <code>TWILIO_WHATSAPP_FROM</code> no <code>backend/.env</code> (veja <code>INTEGRACAO_WHATSAPP.md</code>). Enquanto isso, use o botão WhatsApp de cada cliente.
          </span>
        </div>
      )}
      {config.twilio_configurado && config.sandbox && (
        <div className="vespera-note" data-testid="twilio-sandbox-note">
          <AlertTriangle size={14} />
          <span>Twilio em modo <strong>Sandbox</strong>: só recebe quem enviou “join &lt;código&gt;” para {config.remetente}.</span>
        </div>
      )}

      <div className="vespera-list">
        {itens.map((item) => <LinhaLembrete key={item.id} item={item} config={config} onChange={patch} />)}
      </div>
    </section>
  );
}

===== FILE: frontend/src/components/ServicoInsumos.jsx =====
import { useEffect, useState } from "react";
import { ChevronDown, ChevronUp, Plus, Trash2, Package } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

export default function ServicoInsumos({ servico, insumos }) {
  const toast = useToast();
  const [open, setOpen] = useState(false);
  const [rels, setRels] = useState(null);
  const [form, setForm] = useState({ insumo_id: "", quantidade_utilizada: 1 });

  const load = async () => {
    try { const { data } = await api.get(`/servicos/${servico.id}/insumos`); setRels(data); }
    catch { toast("Erro ao carregar insumos do serviço", "error"); }
  };
  useEffect(() => { if (open && rels === null) load(); /* eslint-disable-next-line */ }, [open]);

  const add = async (e) => {
    e.preventDefault();
    if (!form.insumo_id) { toast("Escolha um insumo", "error"); return; }
    try {
      const { data } = await api.post(`/servicos/${servico.id}/insumos`, { insumo_id: form.insumo_id, quantidade_utilizada: Number(form.quantidade_utilizada) });
      setRels(data);
      setForm({ insumo_id: "", quantidade_utilizada: 1 });
      toast("Insumo vinculado", "success");
    } catch (ex) { toast(ex.response?.data?.detail || "Erro ao vincular", "error"); }
  };

  const remove = async (insumoId) => {
    try { await api.delete(`/servicos/${servico.id}/insumos/${insumoId}`); setRels((v) => v.filter((r) => r.insumo_id !== insumoId)); toast("Vínculo removido", "success"); }
    catch { toast("Erro ao remover", "error"); }
  };

  const disponiveis = insumos.filter((i) => !(rels || []).some((r) => r.insumo_id === i.id));
  const count = rels?.length;

  return (
    <div className="si-wrap">
      <button type="button" className="si-toggle" onClick={() => setOpen((v) => !v)} data-testid={`btn-toggle-insumos-${servico.id}`}>
        <Package size={13} /> Insumos consumidos{typeof count === "number" ? ` (${count})` : ""}
        {open ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
      </button>
      {open && (
        <div className="si-panel" data-testid={`servico-insumos-${servico.id}`}>
          {rels === null && <p className="si-empty">Carregando…</p>}
          {rels?.length === 0 && <p className="si-empty">Nenhum insumo vinculado. Ao concluir um atendimento deste serviço, nada será descontado do estoque.</p>}
          {rels?.map((r) => (
            <div key={r.id} className="si-row" data-testid={`si-${servico.id}-${r.insumo_id}`}>
              <span className="si-name">{r.insumo_nome}</span>
              <span className={`badge ${r.quantidade_atual <= r.quantidade_minima_alerta ? "red" : "green"}`}>{r.quantidade_atual} un em estoque</span>
              <span className="si-qty">−{r.quantidade_utilizada} / atendimento</span>
              <button type="button" className="topbar-icon" onClick={() => remove(r.insumo_id)} data-testid={`btn-del-si-${servico.id}-${r.insumo_id}`} title="Remover vínculo"><Trash2 size={13} /></button>
            </div>
          ))}
          <form className="si-form" onSubmit={add}>
            <select value={form.insumo_id} onChange={(e) => setForm({ ...form, insumo_id: e.target.value })} data-testid={`form-si-insumo-${servico.id}`}>
              <option value="">Escolher insumo…</option>
              {disponiveis.map((i) => <option key={i.id} value={i.id}>{i.nome} ({i.quantidade_atual} un)</option>)}
            </select>
            <input type="number" min="0.1" step="0.1" value={form.quantidade_utilizada} onChange={(e) => setForm({ ...form, quantidade_utilizada: e.target.value })} data-testid={`form-si-qtd-${servico.id}`} title="Quantidade por atendimento" />
            <button type="submit" className="btn-inline small primary" data-testid={`btn-add-si-${servico.id}`}><Plus size={13} /> Vincular</button>
          </form>
        </div>
      )}
    </div>
  );
}

===== FILE: frontend/src/components/ui/accordion.jsx =====
import * as React from "react"
import * as AccordionPrimitive from "@radix-ui/react-accordion"
import { ChevronDown } from "lucide-react"

import { cn } from "@/lib/utils"

const Accordion = AccordionPrimitive.Root

const AccordionItem = React.forwardRef(({ className, ...props }, ref) => (
  <AccordionPrimitive.Item ref={ref} className={cn("border-b", className)} {...props} />
))
AccordionItem.displayName = "AccordionItem"

const AccordionTrigger = React.forwardRef(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Header className="flex">
    <AccordionPrimitive.Trigger
      ref={ref}
      className={cn(
        "flex flex-1 items-center justify-between py-4 text-sm font-medium transition-all hover:underline text-left [&[data-state=open]>svg]:rotate-180",
        className
      )}
      {...props}>
      {children}
      <ChevronDown
        className="h-4 w-4 shrink-0 text-muted-foreground transition-transform duration-200" />
    </AccordionPrimitive.Trigger>
  </AccordionPrimitive.Header>
))
AccordionTrigger.displayName = AccordionPrimitive.Trigger.displayName

const AccordionContent = React.forwardRef(({ className, children, ...props }, ref) => (
  <AccordionPrimitive.Content
    ref={ref}
    className="overflow-hidden text-sm data-[state=closed]:animate-accordion-up data-[state=open]:animate-accordion-down"
    {...props}>
    <div className={cn("pb-4 pt-0", className)}>{children}</div>
  </AccordionPrimitive.Content>
))
AccordionContent.displayName = AccordionPrimitive.Content.displayName

export { Accordion, AccordionItem, AccordionTrigger, AccordionContent }

===== FILE: frontend/src/components/ui/alert-dialog.jsx =====
import * as React from "react"
import * as AlertDialogPrimitive from "@radix-ui/react-alert-dialog"

import { cn } from "@/lib/utils"
import { buttonVariants } from "@/components/ui/button"

const AlertDialog = AlertDialogPrimitive.Root

const AlertDialogTrigger = AlertDialogPrimitive.Trigger

const AlertDialogPortal = AlertDialogPrimitive.Portal

const AlertDialogOverlay = React.forwardRef(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Overlay
    className={cn(
      "fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
    ref={ref} />
))
AlertDialogOverlay.displayName = AlertDialogPrimitive.Overlay.displayName

const AlertDialogContent = React.forwardRef(({ className, ...props }, ref) => (
  <AlertDialogPortal>
    <AlertDialogOverlay />
    <AlertDialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
        className
      )}
      {...props} />
  </AlertDialogPortal>
))
AlertDialogContent.displayName = AlertDialogPrimitive.Content.displayName

const AlertDialogHeader = ({
  className,
  ...props
}) => (
  <div
    className={cn("flex flex-col space-y-2 text-center sm:text-left", className)}
    {...props} />
)
AlertDialogHeader.displayName = "AlertDialogHeader"

const AlertDialogFooter = ({
  className,
  ...props
}) => (
  <div
    className={cn("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2", className)}
    {...props} />
)
AlertDialogFooter.displayName = "AlertDialogFooter"

const AlertDialogTitle = React.forwardRef(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Title ref={ref} className={cn("text-lg font-semibold", className)} {...props} />
))
AlertDialogTitle.displayName = AlertDialogPrimitive.Title.displayName

const AlertDialogDescription = React.forwardRef(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props} />
))
AlertDialogDescription.displayName =
  AlertDialogPrimitive.Description.displayName

const AlertDialogAction = React.forwardRef(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Action ref={ref} className={cn(buttonVariants(), className)} {...props} />
))
AlertDialogAction.displayName = AlertDialogPrimitive.Action.displayName

const AlertDialogCancel = React.forwardRef(({ className, ...props }, ref) => (
  <AlertDialogPrimitive.Cancel
    ref={ref}
    className={cn(buttonVariants({ variant: "outline" }), "mt-2 sm:mt-0", className)}
    {...props} />
))
AlertDialogCancel.displayName = AlertDialogPrimitive.Cancel.displayName

export {
  AlertDialog,
  AlertDialogPortal,
  AlertDialogOverlay,
  AlertDialogTrigger,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogFooter,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogAction,
  AlertDialogCancel,
}

===== FILE: frontend/src/components/ui/alert.jsx =====
import * as React from "react"
import { cva } from "class-variance-authority";

import { cn } from "@/lib/utils"

const alertVariants = cva(
  "relative w-full rounded-lg border px-4 py-3 text-sm [&>svg+div]:translate-y-[-3px] [&>svg]:absolute [&>svg]:left-4 [&>svg]:top-4 [&>svg]:text-foreground [&>svg~*]:pl-7",
  {
    variants: {
      variant: {
        default: "bg-background text-foreground",
        destructive:
          "border-destructive/50 text-destructive dark:border-destructive [&>svg]:text-destructive",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

const Alert = React.forwardRef(({ className, variant, ...props }, ref) => (
  <div
    ref={ref}
    role="alert"
    className={cn(alertVariants({ variant }), className)}
    {...props} />
))
Alert.displayName = "Alert"

const AlertTitle = React.forwardRef(({ className, ...props }, ref) => (
  <h5
    ref={ref}
    className={cn("mb-1 font-medium leading-none tracking-tight", className)}
    {...props} />
))
AlertTitle.displayName = "AlertTitle"

const AlertDescription = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-sm [&_p]:leading-relaxed", className)}
    {...props} />
))
AlertDescription.displayName = "AlertDescription"

export { Alert, AlertTitle, AlertDescription }

===== FILE: frontend/src/components/ui/aspect-ratio.jsx =====
import * as AspectRatioPrimitive from "@radix-ui/react-aspect-ratio"

const AspectRatio = AspectRatioPrimitive.Root

export { AspectRatio }

===== FILE: frontend/src/components/ui/avatar.jsx =====
import * as React from "react"
import * as AvatarPrimitive from "@radix-ui/react-avatar"

import { cn } from "@/lib/utils"

const Avatar = React.forwardRef(({ className, ...props }, ref) => (
  <AvatarPrimitive.Root
    ref={ref}
    className={cn("relative flex h-10 w-10 shrink-0 overflow-hidden rounded-full", className)}
    {...props} />
))
Avatar.displayName = AvatarPrimitive.Root.displayName

const AvatarImage = React.forwardRef(({ className, ...props }, ref) => (
  <AvatarPrimitive.Image
    ref={ref}
    className={cn("aspect-square h-full w-full", className)}
    {...props} />
))
AvatarImage.displayName = AvatarPrimitive.Image.displayName

const AvatarFallback = React.forwardRef(({ className, ...props }, ref) => (
  <AvatarPrimitive.Fallback
    ref={ref}
    className={cn(
      "flex h-full w-full items-center justify-center rounded-full bg-muted",
      className
    )}
    {...props} />
))
AvatarFallback.displayName = AvatarPrimitive.Fallback.displayName

export { Avatar, AvatarImage, AvatarFallback }

===== FILE: frontend/src/components/ui/badge.jsx =====
import * as React from "react"
import { cva } from "class-variance-authority";

import { cn } from "@/lib/utils"

const badgeVariants = cva(
  "inline-flex items-center rounded-md border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-primary text-primary-foreground shadow hover:bg-primary/80",
        secondary:
          "border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80",
        destructive:
          "border-transparent bg-destructive text-destructive-foreground shadow hover:bg-destructive/80",
        outline: "text-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

function Badge({
  className,
  variant,
  ...props
}) {
  return (<div className={cn(badgeVariants({ variant }), className)} {...props} />);
}

export { Badge, badgeVariants }

===== FILE: frontend/src/components/ui/breadcrumb.jsx =====
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { ChevronRight, MoreHorizontal } from "lucide-react"

import { cn } from "@/lib/utils"

const Breadcrumb = React.forwardRef(
  ({ ...props }, ref) => <nav ref={ref} aria-label="breadcrumb" {...props} />
)
Breadcrumb.displayName = "Breadcrumb"

const BreadcrumbList = React.forwardRef(({ className, ...props }, ref) => (
  <ol
    ref={ref}
    className={cn(
      "flex flex-wrap items-center gap-1.5 break-words text-sm text-muted-foreground sm:gap-2.5",
      className
    )}
    {...props} />
))
BreadcrumbList.displayName = "BreadcrumbList"

const BreadcrumbItem = React.forwardRef(({ className, ...props }, ref) => (
  <li
    ref={ref}
    className={cn("inline-flex items-center gap-1.5", className)}
    {...props} />
))
BreadcrumbItem.displayName = "BreadcrumbItem"

const BreadcrumbLink = React.forwardRef(({ asChild, className, ...props }, ref) => {
  const Comp = asChild ? Slot : "a"

  return (
    <Comp
      ref={ref}
      className={cn("transition-colors hover:text-foreground", className)}
      {...props} />
  );
})
BreadcrumbLink.displayName = "BreadcrumbLink"

const BreadcrumbPage = React.forwardRef(({ className, ...props }, ref) => (
  <span
    ref={ref}
    role="link"
    aria-disabled="true"
    aria-current="page"
    className={cn("font-normal text-foreground", className)}
    {...props} />
))
BreadcrumbPage.displayName = "BreadcrumbPage"

const BreadcrumbSeparator = ({
  children,
  className,
  ...props
}) => (
  <li
    role="presentation"
    aria-hidden="true"
    className={cn("[&>svg]:w-3.5 [&>svg]:h-3.5", className)}
    {...props}>
    {children ?? <ChevronRight />}
  </li>
)
BreadcrumbSeparator.displayName = "BreadcrumbSeparator"

const BreadcrumbEllipsis = ({
  className,
  ...props
}) => (
  <span
    role="presentation"
    aria-hidden="true"
    className={cn("flex h-9 w-9 items-center justify-center", className)}
    {...props}>
    <MoreHorizontal className="h-4 w-4" />
    <span className="sr-only">More</span>
  </span>
)
BreadcrumbEllipsis.displayName = "BreadcrumbElipssis"

export {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbPage,
  BreadcrumbSeparator,
  BreadcrumbEllipsis,
}

===== FILE: frontend/src/components/ui/button.jsx =====
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva } from "class-variance-authority";

import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default:
          "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive:
          "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline:
          "border border-input shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary:
          "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

const Button = React.forwardRef(({ className, variant, size, asChild = false, ...props }, ref) => {
  const Comp = asChild ? Slot : "button"
  return (
    <Comp
      className={cn(buttonVariants({ variant, size, className }))}
      ref={ref}
      {...props} />
  );
})
Button.displayName = "Button"

export { Button, buttonVariants }

===== FILE: frontend/src/components/ui/calendar.jsx =====
import * as React from "react"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { DayPicker } from "react-day-picker"

import { cn } from "@/lib/utils"
import { buttonVariants } from "@/components/ui/button"

function Calendar({
  className,
  classNames,
  showOutsideDays = true,
  ...props
}) {
  return (
    <DayPicker
      showOutsideDays={showOutsideDays}
      className={cn("p-3", className)}
      classNames={{
        months: "flex flex-col sm:flex-row space-y-4 sm:space-x-4 sm:space-y-0",
        month: "space-y-4",
        caption: "flex justify-center pt-1 relative items-center",
        caption_label: "text-sm font-medium",
        nav: "space-x-1 flex items-center",
        nav_button: cn(
          buttonVariants({ variant: "outline" }),
          "h-7 w-7 bg-transparent p-0 opacity-50 hover:opacity-100"
        ),
        nav_button_previous: "absolute left-1",
        nav_button_next: "absolute right-1",
        table: "w-full border-collapse space-y-1",
        head_row: "flex",
        head_cell:
          "text-muted-foreground rounded-md w-8 font-normal text-[0.8rem]",
        row: "flex w-full mt-2",
        cell: cn(
          "relative p-0 text-center text-sm focus-within:relative focus-within:z-20 [&:has([aria-selected])]:bg-accent [&:has([aria-selected].day-outside)]:bg-accent/50 [&:has([aria-selected].day-range-end)]:rounded-r-md",
          props.mode === "range"
            ? "[&:has(>.day-range-end)]:rounded-r-md [&:has(>.day-range-start)]:rounded-l-md first:[&:has([aria-selected])]:rounded-l-md last:[&:has([aria-selected])]:rounded-r-md"
            : "[&:has([aria-selected])]:rounded-md"
        ),
        day: cn(
          buttonVariants({ variant: "ghost" }),
          "h-8 w-8 p-0 font-normal aria-selected:opacity-100"
        ),
        day_range_start: "day-range-start",
        day_range_end: "day-range-end",
        day_selected:
          "bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground focus:bg-primary focus:text-primary-foreground",
        day_today: "bg-accent text-accent-foreground",
        day_outside:
          "day-outside text-muted-foreground aria-selected:bg-accent/50 aria-selected:text-muted-foreground",
        day_disabled: "text-muted-foreground opacity-50",
        day_range_middle:
          "aria-selected:bg-accent aria-selected:text-accent-foreground",
        day_hidden: "invisible",
        ...classNames,
      }}
      components={{
        IconLeft: ({ className, ...props }) => (
          <ChevronLeft className={cn("h-4 w-4", className)} {...props} />
        ),
        IconRight: ({ className, ...props }) => (
          <ChevronRight className={cn("h-4 w-4", className)} {...props} />
        ),
      }}
      {...props} />
  );
}
Calendar.displayName = "Calendar"

export { Calendar }

===== FILE: frontend/src/components/ui/card.jsx =====
import * as React from "react"

import { cn } from "@/lib/utils"

const Card = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("rounded-xl border bg-card text-card-foreground shadow", className)}
    {...props} />
))
Card.displayName = "Card"

const CardHeader = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col space-y-1.5 p-6", className)}
    {...props} />
))
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("font-semibold leading-none tracking-tight", className)}
    {...props} />
))
CardTitle.displayName = "CardTitle"

const CardDescription = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props} />
))
CardDescription.displayName = "CardDescription"

const CardContent = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
))
CardContent.displayName = "CardContent"

const CardFooter = React.forwardRef(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex items-center p-6 pt-0", className)}
    {...props} />
))
CardFooter.displayName = "CardFooter"

export { Card, CardHeader, CardFooter, CardTitle, CardDescription, CardContent }

===== FILE: frontend/src/components/ui/carousel.jsx =====
import * as React from "react"
import useEmblaCarousel from "embla-carousel-react";
import { ArrowLeft, ArrowRight } from "lucide-react"

import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

const CarouselContext = React.createContext(null)

function useCarousel() {
  const context = React.useContext(CarouselContext)

  if (!context) {
    throw new Error("useCarousel must be used within a <Carousel />")
  }

  return context
}

const Carousel = React.forwardRef((
  {
    orientation = "horizontal",
    opts,
    setApi,
    plugins,
    className,
    children,
    ...props
  },
  ref
) => {
  const [carouselRef, api] = useEmblaCarousel({
    ...opts,
    axis: orientation === "horizontal" ? "x" : "y",
  }, plugins)
  const [canScrollPrev, setCanScrollPrev] = React.useState(false)
  const [canScrollNext, setCanScrollNext] = React.useState(false)

  const onSelect = React.useCallback((api) => {
    if (!api) {
      return
    }

    setCanScrollPrev(api.canScrollPrev())
    setCanScrollNext(api.canScrollNext())
  }, [])

  const scrollPrev = React.useCallback(() => {
    api?.scrollPrev()
  }, [api])

  const scrollNext = React.useCallback(() => {
    api?.scrollNext()
  }, [api])

  const handleKeyDown = React.useCallback((event) => {
    if (event.key === "ArrowLeft") {
      event.preventDefault()
      scrollPrev()
    } else if (event.key === "ArrowRight") {
      event.preventDefault()
      scrollNext()
    }
  }, [scrollPrev, scrollNext])

  React.useEffect(() => {
    if (!api || !setApi) {
      return
    }

    setApi(api)
  }, [api, setApi])

  React.useEffect(() => {
    if (!api) {
      return
    }

    onSelect(api)
    api.on("reInit", onSelect)
    api.on("select", onSelect)

    return () => {
      api?.off("select", onSelect)
    };
  }, [api, onSelect])

  return (
    <CarouselContext.Provider
      value={{
        carouselRef,
        api: api,
        opts,
        orientation:
          orientation || (opts?.axis === "y" ? "vertical" : "horizontal"),
        scrollPrev,
        scrollNext,
        canScrollPrev,
        canScrollNext,
      }}>
      <div
        ref={ref}
        onKeyDownCapture={handleKeyDown}
        className={cn("relative", className)}
        role="region"
        aria-roledescription="carousel"
        {...props}>
        {children}
      </div>
    </CarouselContext.Provider>
  );
})
Carousel.displayName = "Carousel"

const CarouselContent = React.forwardRef(({ className, ...props }, ref) => {
  const { carouselRef, orientation } = useCarousel()

  return (
    <div ref={carouselRef} className="overflow-hidden">
      <div
        ref={ref}
        className={cn(
          "flex",
          orientation === "horizontal" ? "-ml-4" : "-mt-4 flex-col",
          className
        )}
        {...props} />
    </div>
  );
})
CarouselContent.displayName = "CarouselContent"

const CarouselItem = React.forwardRef(({ className, ...props }, ref) => {
  const { orientation } = useCarousel()

  return (
    <div
      ref={ref}
      role="group"
      aria-roledescription="slide"
      className={cn(
        "min-w-0 shrink-0 grow-0 basis-full",
        orientation === "horizontal" ? "pl-4" : "pt-4",
        className
      )}
      {...props} />
  );
})
CarouselItem.displayName = "CarouselItem"

const CarouselPrevious = React.forwardRef(({ className, variant = "outline", size = "icon", ...props }, ref) => {
  const { orientation, scrollPrev, canScrollPrev } = useCarousel()

  return (
    <Button
      ref={ref}
      variant={variant}
      size={size}
      className={cn("absolute  h-8 w-8 rounded-full", orientation === "horizontal"
        ? "-left-12 top-1/2 -translate-y-1/2"
        : "-top-12 left-1/2 -translate-x-1/2 rotate-90", className)}
      disabled={!canScrollPrev}
      onClick={scrollPrev}
      {...props}>
      <ArrowLeft className="h-4 w-4" />
      <span className="sr-only">Previous slide</span>
    </Button>
  );
})
CarouselPrevious.displayName = "CarouselPrevious"

const CarouselNext = React.forwardRef(({ className, variant = "outline", size = "icon", ...props }, ref) => {
  const { orientation, scrollNext, canScrollNext } = useCarousel()

  return (
    <Button
      ref={ref}
      variant={variant}
      size={size}
      className={cn("absolute h-8 w-8 rounded-full", orientation === "horizontal"
        ? "-right-12 top-1/2 -translate-y-1/2"
        : "-bottom-12 left-1/2 -translate-x-1/2 rotate-90", className)}
      disabled={!canScrollNext}
      onClick={scrollNext}
      {...props}>
      <ArrowRight className="h-4 w-4" />
      <span className="sr-only">Next slide</span>
    </Button>
  );
})
CarouselNext.displayName = "CarouselNext"

export { Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext };

===== FILE: frontend/src/components/ui/checkbox.jsx =====
import * as React from "react"
import * as CheckboxPrimitive from "@radix-ui/react-checkbox"
import { Check } from "lucide-react"

import { cn } from "@/lib/utils"

const Checkbox = React.forwardRef(({ className, ...props }, ref) => (
  <CheckboxPrimitive.Root
    ref={ref}
    className={cn(
      "peer h-4 w-4 shrink-0 rounded-sm border border-primary shadow focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=checked]:text-primary-foreground",
      className
    )}
    {...props}>
    <CheckboxPrimitive.Indicator className={cn("flex items-center justify-center text-current")}>
      <Check className="h-4 w-4" />
    </CheckboxPrimitive.Indicator>
  </CheckboxPrimitive.Root>
))
Checkbox.displayName = CheckboxPrimitive.Root.displayName

export { Checkbox }

===== FILE: frontend/src/components/ui/collapsible.jsx =====
import * as CollapsiblePrimitive from "@radix-ui/react-collapsible"

const Collapsible = CollapsiblePrimitive.Root

const CollapsibleTrigger = CollapsiblePrimitive.CollapsibleTrigger

const CollapsibleContent = CollapsiblePrimitive.CollapsibleContent

export { Collapsible, CollapsibleTrigger, CollapsibleContent }

===== FILE: frontend/src/components/ui/command.jsx =====
import * as React from "react"
import { Command as CommandPrimitive } from "cmdk"
import { Search } from "lucide-react"

import { cn } from "@/lib/utils"
import { Dialog, DialogContent } from "@/components/ui/dialog"

const Command = React.forwardRef(({ className, ...props }, ref) => (
  <CommandPrimitive
    ref={ref}
    className={cn(
      "flex h-full w-full flex-col overflow-hidden rounded-md bg-popover text-popover-foreground",
      className
    )}
    {...props} />
))
Command.displayName = CommandPrimitive.displayName

const CommandDialog = ({
  children,
  ...props
}) => {
  return (
    <Dialog {...props}>
      <DialogContent className="overflow-hidden p-0">
        <Command
          className="[&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:font-medium [&_[cmdk-group-heading]]:text-muted-foreground [&_[cmdk-group]:not([hidden])_~[cmdk-group]]:pt-0 [&_[cmdk-group]]:px-2 [&_[cmdk-input-wrapper]_svg]:h-5 [&_[cmdk-input-wrapper]_svg]:w-5 [&_[cmdk-input]]:h-12 [&_[cmdk-item]]:px-2 [&_[cmdk-item]]:py-3 [&_[cmdk-item]_svg]:h-5 [&_[cmdk-item]_svg]:w-5">
          {children}
        </Command>
      </DialogContent>
    </Dialog>
  );
}

const CommandInput = React.forwardRef(({ className, ...props }, ref) => (
  <div className="flex items-center border-b px-3" cmdk-input-wrapper="">
    <Search className="mr-2 h-4 w-4 shrink-0 opacity-50" />
    <CommandPrimitive.Input
      ref={ref}
      className={cn(
        "flex h-10 w-full rounded-md bg-transparent py-3 text-sm outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props} />
  </div>
))

CommandInput.displayName = CommandPrimitive.Input.displayName

const CommandList = React.forwardRef(({ className, ...props }, ref) => (
  <CommandPrimitive.List
    ref={ref}
    className={cn("max-h-[300px] overflow-y-auto overflow-x-hidden", className)}
    {...props} />
))

CommandList.displayName = CommandPrimitive.List.displayName

const CommandEmpty = React.forwardRef((props, ref) => (
  <CommandPrimitive.Empty ref={ref} className="py-6 text-center text-sm" {...props} />
))

CommandEmpty.displayName = CommandPrimitive.Empty.displayName

const CommandGroup = React.forwardRef(({ className, ...props }, ref) => (
  <CommandPrimitive.Group
    ref={ref}
    className={cn(
      "overflow-hidden p-1 text-foreground [&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:py-1.5 [&_[cmdk-group-heading]]:text-xs [&_[cmdk-group-heading]]:font-medium [&_[cmdk-group-heading]]:text-muted-foreground",
      className
    )}
    {...props} />
))

CommandGroup.displayName = CommandPrimitive.Group.displayName

const CommandSeparator = React.forwardRef(({ className, ...props }, ref) => (
  <CommandPrimitive.Separator ref={ref} className={cn("-mx-1 h-px bg-border", className)} {...props} />
))
CommandSeparator.displayName = CommandPrimitive.Separator.displayName

const CommandItem = React.forwardRef(({ className, ...props }, ref) => (
  <CommandPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default gap-2 select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none data-[disabled=true]:pointer-events-none data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground data-[disabled=true]:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
      className
    )}
    {...props} />
))

CommandItem.displayName = CommandPrimitive.Item.displayName

const CommandShortcut = ({
  className,
  ...props
}) => {
  return (
    <span
      className={cn("ml-auto text-xs tracking-widest text-muted-foreground", className)}
      {...props} />
  );
}
CommandShortcut.displayName = "CommandShortcut"

export {
  Command,
  CommandDialog,
  CommandInput,
  CommandList,
  CommandEmpty,
  CommandGroup,
  CommandItem,
  CommandShortcut,
  CommandSeparator,
}

===== FILE: frontend/src/components/ui/context-menu.jsx =====
import * as React from "react"
import * as ContextMenuPrimitive from "@radix-ui/react-context-menu"
import { Check, ChevronRight, Circle } from "lucide-react"

import { cn } from "@/lib/utils"

const ContextMenu = ContextMenuPrimitive.Root

const ContextMenuTrigger = ContextMenuPrimitive.Trigger

const ContextMenuGroup = ContextMenuPrimitive.Group

const ContextMenuPortal = ContextMenuPrimitive.Portal

const ContextMenuSub = ContextMenuPrimitive.Sub

const ContextMenuRadioGroup = ContextMenuPrimitive.RadioGroup

const ContextMenuSubTrigger = React.forwardRef(({ className, inset, children, ...props }, ref) => (
  <ContextMenuPrimitive.SubTrigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
      inset && "pl-8",
      className
    )}
    {...props}>
    {children}
    <ChevronRight className="ml-auto h-4 w-4" />
  </ContextMenuPrimitive.SubTrigger>
))
ContextMenuSubTrigger.displayName = ContextMenuPrimitive.SubTrigger.displayName

const ContextMenuSubContent = React.forwardRef(({ className, ...props }, ref) => (
  <ContextMenuPrimitive.SubContent
    ref={ref}
    className={cn(
      "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-context-menu-content-transform-origin]",
      className
    )}
    {...props} />
))
ContextMenuSubContent.displayName = ContextMenuPrimitive.SubContent.displayName

const ContextMenuContent = React.forwardRef(({ className, ...props }, ref) => (
  <ContextMenuPrimitive.Portal>
    <ContextMenuPrimitive.Content
      ref={ref}
      className={cn(
        "z-50 max-h-[--radix-context-menu-content-available-height] min-w-[8rem] overflow-y-auto overflow-x-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-context-menu-content-transform-origin]",
        className
      )}
      {...props} />
  </ContextMenuPrimitive.Portal>
))
ContextMenuContent.displayName = ContextMenuPrimitive.Content.displayName

const ContextMenuItem = React.forwardRef(({ className, inset, ...props }, ref) => (
  <ContextMenuPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      inset && "pl-8",
      className
    )}
    {...props} />
))
ContextMenuItem.displayName = ContextMenuPrimitive.Item.displayName

const ContextMenuCheckboxItem = React.forwardRef(({ className, children, checked, ...props }, ref) => (
  <ContextMenuPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    checked={checked}
    {...props}>
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <ContextMenuPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </ContextMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </ContextMenuPrimitive.CheckboxItem>
))
ContextMenuCheckboxItem.displayName =
  ContextMenuPrimitive.CheckboxItem.displayName

const ContextMenuRadioItem = React.forwardRef(({ className, children, ...props }, ref) => (
  <ContextMenuPrimitive.RadioItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}>
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <ContextMenuPrimitive.ItemIndicator>
        <Circle className="h-4 w-4 fill-current" />
      </ContextMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </ContextMenuPrimitive.RadioItem>
))
ContextMenuRadioItem.displayName = ContextMenuPrimitive.RadioItem.displayName

const ContextMenuLabel = React.forwardRef(({ className, inset, ...props }, ref) => (
  <ContextMenuPrimitive.Label
    ref={ref}
    className={cn(
      "px-2 py-1.5 text-sm font-semibold text-foreground",
      inset && "pl-8",
      className
    )}
    {...props} />
))
ContextMenuLabel.displayName = ContextMenuPrimitive.Label.displayName

const ContextMenuSeparator = React.forwardRef(({ className, ...props }, ref) => (
  <ContextMenuPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-border", className)}
    {...props} />
))
ContextMenuSeparator.displayName = ContextMenuPrimitive.Separator.displayName

const ContextMenuShortcut = ({
  className,
  ...props
}) => {
  return (
    <span
      className={cn("ml-auto text-xs tracking-widest text-muted-foreground", className)}
      {...props} />
  );
}
ContextMenuShortcut.displayName = "ContextMenuShortcut"

export {
  ContextMenu,
  ContextMenuTrigger,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuCheckboxItem,
  ContextMenuRadioItem,
  ContextMenuLabel,
  ContextMenuSeparator,
  ContextMenuShortcut,
  ContextMenuGroup,
  ContextMenuPortal,
  ContextMenuSub,
  ContextMenuSubContent,
  ContextMenuSubTrigger,
  ContextMenuRadioGroup,
}

===== FILE: frontend/src/components/ui/dialog.jsx =====
import * as React from "react"
import * as DialogPrimitive from "@radix-ui/react-dialog"
import { X } from "lucide-react"

import { cn } from "@/lib/utils"

const Dialog = DialogPrimitive.Root

const DialogTrigger = DialogPrimitive.Trigger

const DialogPortal = DialogPrimitive.Portal

const DialogClose = DialogPrimitive.Close

const DialogOverlay = React.forwardRef(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      "fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props} />
))
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName

const DialogContent = React.forwardRef(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-background p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg",
        className
      )}
      {...props}>
      {children}
      <DialogPrimitive.Close
        className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
))
DialogContent.displayName = DialogPrimitive.Content.displayName

const DialogHeader = ({
  className,
  ...props
}) => (
  <div
    className={cn("flex flex-col space-y-1.5 text-center sm:text-left", className)}
    {...props} />
)
DialogHeader.displayName = "DialogHeader"

const DialogFooter = ({
  className,
  ...props
}) => (
  <div
    className={cn("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2", className)}
    {...props} />
)
DialogFooter.displayName = "DialogFooter"

const DialogTitle = React.forwardRef(({ className, ...props }, ref) => (
  <DialogPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold leading-none tracking-tight", className)}
    {...props} />
))
DialogTitle.displayName = DialogPrimitive.Title.displayName

const DialogDescription = React.forwardRef(({ className, ...props }, ref) => (
  <DialogPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props} />
))
DialogDescription.displayName = DialogPrimitive.Description.displayName

export {
  Dialog,
  DialogPortal,
  DialogOverlay,
  DialogTrigger,
  DialogClose,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
}

===== FILE: frontend/src/components/ui/drawer.jsx =====
import * as React from "react"
import { Drawer as DrawerPrimitive } from "vaul"

import { cn } from "@/lib/utils"

const Drawer = ({
  shouldScaleBackground = true,
  ...props
}) => (
  <DrawerPrimitive.Root shouldScaleBackground={shouldScaleBackground} {...props} />
)
Drawer.displayName = "Drawer"

const DrawerTrigger = DrawerPrimitive.Trigger

const DrawerPortal = DrawerPrimitive.Portal

const DrawerClose = DrawerPrimitive.Close

const DrawerOverlay = React.forwardRef(({ className, ...props }, ref) => (
  <DrawerPrimitive.Overlay
    ref={ref}
    className={cn("fixed inset-0 z-50 bg-black/80", className)}
    {...props} />
))
DrawerOverlay.displayName = DrawerPrimitive.Overlay.displayName

const DrawerContent = React.forwardRef(({ className, children, ...props }, ref) => (
  <DrawerPortal>
    <DrawerOverlay />
    <DrawerPrimitive.Content
      ref={ref}
      className={cn(
        "fixed inset-x-0 bottom-0 z-50 mt-24 flex h-auto flex-col rounded-t-[10px] border bg-background",
        className
      )}
      {...props}>
      <div className="mx-auto mt-4 h-2 w-[100px] rounded-full bg-muted" />
      {children}
    </DrawerPrimitive.Content>
  </DrawerPortal>
))
DrawerContent.displayName = "DrawerContent"

const DrawerHeader = ({
  className,
  ...props
}) => (
  <div
    className={cn("grid gap-1.5 p-4 text-center sm:text-left", className)}
    {...props} />
)
DrawerHeader.displayName = "DrawerHeader"

const DrawerFooter = ({
  className,
  ...props
}) => (
  <div className={cn("mt-auto flex flex-col gap-2 p-4", className)} {...props} />
)
DrawerFooter.displayName = "DrawerFooter"

const DrawerTitle = React.forwardRef(({ className, ...props }, ref) => (
  <DrawerPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold leading-none tracking-tight", className)}
    {...props} />
))
DrawerTitle.displayName = DrawerPrimitive.Title.displayName

const DrawerDescription = React.forwardRef(({ className, ...props }, ref) => (
  <DrawerPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props} />
))
DrawerDescription.displayName = DrawerPrimitive.Description.displayName

export {
  Drawer,
  DrawerPortal,
  DrawerOverlay,
  DrawerTrigger,
  DrawerClose,
  DrawerContent,
  DrawerHeader,
  DrawerFooter,
  DrawerTitle,
  DrawerDescription,
}

===== FILE: frontend/src/components/ui/dropdown-menu.jsx =====
import * as React from "react"
import * as DropdownMenuPrimitive from "@radix-ui/react-dropdown-menu"
import { Check, ChevronRight, Circle } from "lucide-react"

import { cn } from "@/lib/utils"

const DropdownMenu = DropdownMenuPrimitive.Root

const DropdownMenuTrigger = DropdownMenuPrimitive.Trigger

const DropdownMenuGroup = DropdownMenuPrimitive.Group

const DropdownMenuPortal = DropdownMenuPrimitive.Portal

const DropdownMenuSub = DropdownMenuPrimitive.Sub

const DropdownMenuRadioGroup = DropdownMenuPrimitive.RadioGroup

const DropdownMenuSubTrigger = React.forwardRef(({ className, inset, children, ...props }, ref) => (
  <DropdownMenuPrimitive.SubTrigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent data-[state=open]:bg-accent [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
      inset && "pl-8",
      className
    )}
    {...props}>
    {children}
    <ChevronRight className="ml-auto" />
  </DropdownMenuPrimitive.SubTrigger>
))
DropdownMenuSubTrigger.displayName =
  DropdownMenuPrimitive.SubTrigger.displayName

const DropdownMenuSubContent = React.forwardRef(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.SubContent
    ref={ref}
    className={cn(
      "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-dropdown-menu-content-transform-origin]",
      className
    )}
    {...props} />
))
DropdownMenuSubContent.displayName =
  DropdownMenuPrimitive.SubContent.displayName

const DropdownMenuContent = React.forwardRef(({ className, sideOffset = 4, ...props }, ref) => (
  <DropdownMenuPrimitive.Portal>
    <DropdownMenuPrimitive.Content
      ref={ref}
      sideOffset={sideOffset}
      className={cn(
        "z-50 max-h-[var(--radix-dropdown-menu-content-available-height)] min-w-[8rem] overflow-y-auto overflow-x-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md",
        "data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-dropdown-menu-content-transform-origin]",
        className
      )}
      {...props} />
  </DropdownMenuPrimitive.Portal>
))
DropdownMenuContent.displayName = DropdownMenuPrimitive.Content.displayName

const DropdownMenuItem = React.forwardRef(({ className, inset, ...props }, ref) => (
  <DropdownMenuPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center gap-2 rounded-sm px-2 py-1.5 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50 [&>svg]:size-4 [&>svg]:shrink-0",
      inset && "pl-8",
      className
    )}
    {...props} />
))
DropdownMenuItem.displayName = DropdownMenuPrimitive.Item.displayName

const DropdownMenuCheckboxItem = React.forwardRef(({ className, children, checked, ...props }, ref) => (
  <DropdownMenuPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    checked={checked}
    {...props}>
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <DropdownMenuPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </DropdownMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </DropdownMenuPrimitive.CheckboxItem>
))
DropdownMenuCheckboxItem.displayName =
  DropdownMenuPrimitive.CheckboxItem.displayName

const DropdownMenuRadioItem = React.forwardRef(({ className, children, ...props }, ref) => (
  <DropdownMenuPrimitive.RadioItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none transition-colors focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}>
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <DropdownMenuPrimitive.ItemIndicator>
        <Circle className="h-2 w-2 fill-current" />
      </DropdownMenuPrimitive.ItemIndicator>
    </span>
    {children}
  </DropdownMenuPrimitive.RadioItem>
))
DropdownMenuRadioItem.displayName = DropdownMenuPrimitive.RadioItem.displayName

const DropdownMenuLabel = React.forwardRef(({ className, inset, ...props }, ref) => (
  <DropdownMenuPrimitive.Label
    ref={ref}
    className={cn("px-2 py-1.5 text-sm font-semibold", inset && "pl-8", className)}
    {...props} />
))
DropdownMenuLabel.displayName = DropdownMenuPrimitive.Label.displayName

const DropdownMenuSeparator = React.forwardRef(({ className, ...props }, ref) => (
  <DropdownMenuPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-muted", className)}
    {...props} />
))
DropdownMenuSeparator.displayName = DropdownMenuPrimitive.Separator.displayName

const DropdownMenuShortcut = ({
  className,
  ...props
}) => {
  return (
    <span
      className={cn("ml-auto text-xs tracking-widest opacity-60", className)}
      {...props} />
  );
}
DropdownMenuShortcut.displayName = "DropdownMenuShortcut"

export {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuCheckboxItem,
  DropdownMenuRadioItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuShortcut,
  DropdownMenuGroup,
  DropdownMenuPortal,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
  DropdownMenuRadioGroup,
}

===== FILE: frontend/src/components/ui/form.jsx =====
import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { Controller, FormProvider, useFormContext } from "react-hook-form";

import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"

const Form = FormProvider

const FormFieldContext = React.createContext({})

const FormField = (
  {
    ...props
  }
) => {
  return (
    <FormFieldContext.Provider value={{ name: props.name }}>
      <Controller {...props} />
    </FormFieldContext.Provider>
  );
}

const useFormField = () => {
  const fieldContext = React.useContext(FormFieldContext)
  const itemContext = React.useContext(FormItemContext)
  const { getFieldState, formState } = useFormContext()

  const fieldState = getFieldState(fieldContext.name, formState)

  if (!fieldContext) {
    throw new Error("useFormField should be used within <FormField>")
  }

  const { id } = itemContext

  return {
    id,
    name: fieldContext.name,
    formItemId: `${id}-form-item`,
    formDescriptionId: `${id}-form-item-description`,
    formMessageId: `${id}-form-item-message`,
    ...fieldState,
  }
}

const FormItemContext = React.createContext({})

const FormItem = React.forwardRef(({ className, ...props }, ref) => {
  const id = React.useId()

  return (
    <FormItemContext.Provider value={{ id }}>
      <div ref={ref} className={cn("space-y-2", className)} {...props} />
    </FormItemContext.Provider>
  );
})
FormItem.displayName = "FormItem"

const FormLabel = React.forwardRef(({ className, ...props }, ref) => {
  const { error, formItemId } = useFormField()

  return (
    <Label
      ref={ref}
      className={cn(error && "text-destructive", className)}
      htmlFor={formItemId}
      {...props} />
  );
})
FormLabel.displayName = "FormLabel"

const FormControl = React.forwardRef(({ ...props }, ref) => {
  const { error, formItemId, formDescriptionId, formMessageId } = useFormField()

  return (
    <Slot
      ref={ref}
      id={formItemId}
      aria-describedby={
        !error
          ? `${formDescriptionId}`
          : `${formDescriptionId} ${formMessageId}`
      }
      aria-invalid={!!error}
      {...props} />
  );
})
FormControl.displayName = "FormControl"

const FormDescription = React.forwardRef(({ className, ...props }, ref) => {
  const { formDescriptionId } = useFormField()

  return (
    <p
      ref={ref}
      id={formDescriptionId}
      className={cn("text-[0.8rem] text-muted-foreground", className)}
      {...props} />
  );
})
FormDescription.displayName = "FormDescription"

const FormMessage = React.forwardRef(({ className, children, ...props }, ref) => {
  const { error, formMessageId } = useFormField()
  const body = error ? String(error?.message ?? "") : children

  if (!body) {
    return null
  }

  return (
    <p
      ref={ref}
      id={formMessageId}
      className={cn("text-[0.8rem] font-medium text-destructive", className)}
      {...props}>
      {body}
    </p>
  );
})
FormMessage.displayName = "FormMessage"

export {
  useFormField,
  Form,
  FormItem,
  FormLabel,
  FormControl,
  FormDescription,
  FormMessage,
  FormField,
}

===== FILE: frontend/src/components/ui/hover-card.jsx =====
import * as React from "react"
import * as HoverCardPrimitive from "@radix-ui/react-hover-card"

import { cn } from "@/lib/utils"

const HoverCard = HoverCardPrimitive.Root

const HoverCardTrigger = HoverCardPrimitive.Trigger

const HoverCardContent = React.forwardRef(({ className, align = "center", sideOffset = 4, ...props }, ref) => (
  <HoverCardPrimitive.Content
    ref={ref}
    align={align}
    sideOffset={sideOffset}
    className={cn(
      "z-50 w-64 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-hover-card-content-transform-origin]",
      className
    )}
    {...props} />
))
HoverCardContent.displayName = HoverCardPrimitive.Content.displayName

export { HoverCard, HoverCardTrigger, HoverCardContent }

===== FILE: frontend/src/components/ui/input-otp.jsx =====
import * as React from "react"
import { OTPInput, OTPInputContext } from "input-otp"
import { Minus } from "lucide-react"

import { cn } from "@/lib/utils"

const InputOTP = React.forwardRef(({ className, containerClassName, ...props }, ref) => (
  <OTPInput
    ref={ref}
    containerClassName={cn("flex items-center gap-2 has-[:disabled]:opacity-50", containerClassName)}
    className={cn("disabled:cursor-not-allowed", className)}
    {...props} />
))
InputOTP.displayName = "InputOTP"

const InputOTPGroup = React.forwardRef(({ className, ...props }, ref) => (
  <div ref={ref} className={cn("flex items-center", className)} {...props} />
))
InputOTPGroup.displayName = "InputOTPGroup"

const InputOTPSlot = React.forwardRef(({ index, className, ...props }, ref) => {
  const inputOTPContext = React.useContext(OTPInputContext)
  const { char, hasFakeCaret, isActive } = inputOTPContext.slots[index]

  return (
    <div
      ref={ref}
      className={cn(
        "relative flex h-9 w-9 items-center justify-center border-y border-r border-input text-sm shadow-sm transition-all first:rounded-l-md first:border-l last:rounded-r-md",
        isActive && "z-10 ring-1 ring-ring",
        className
      )}
      {...props}>
      {char}
      {hasFakeCaret && (
        <div
          className="pointer-events-none absolute inset-0 flex items-center justify-center">
          <div className="h-4 w-px animate-caret-blink bg-foreground duration-1000" />
        </div>
      )}
    </div>
  );
})
InputOTPSlot.displayName = "InputOTPSlot"

const InputOTPSeparator = React.forwardRef(({ ...props }, ref) => (
  <div ref={ref} role="separator" {...props}>
    <Minus />
  </div>
))
InputOTPSeparator.displayName = "InputOTPSeparator"

export { InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator }

===== FILE: frontend/src/components/ui/input.jsx =====
import * as React from "react"

import { cn } from "@/lib/utils"

const Input = React.forwardRef(({ className, type, ...props }, ref) => {
  return (
    <input
      type={type}
      className={cn(
        "flex h-9 w-full rounded-md border border-input bg-transparent px-3 py-1 text-base shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
        className
      )}
      ref={ref}
      {...props} />
  );
})
Input.displayName = "Input"

export { Input }

===== FILE: frontend/src/components/ui/label.jsx =====
import * as React from "react"
import * as LabelPrimitive from "@radix-ui/react-label"
import { cva } from "class-variance-authority";

import { cn } from "@/lib/utils"

const labelVariants = cva(
  "text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
)

const Label = React.forwardRef(({ className, ...props }, ref) => (
  <LabelPrimitive.Root ref={ref} className={cn(labelVariants(), className)} {...props} />
))
Label.displayName = LabelPrimitive.Root.displayName

export { Label }

===== FILE: frontend/src/components/ui/menubar.jsx =====
import * as React from "react"
import * as MenubarPrimitive from "@radix-ui/react-menubar"
import { Check, ChevronRight, Circle } from "lucide-react"

import { cn } from "@/lib/utils"

function MenubarMenu({
  ...props
}) {
  return <MenubarPrimitive.Menu {...props} />;
}

function MenubarGroup({
  ...props
}) {
  return <MenubarPrimitive.Group {...props} />;
}

function MenubarPortal({
  ...props
}) {
  return <MenubarPrimitive.Portal {...props} />;
}

function MenubarRadioGroup({
  ...props
}) {
  return <MenubarPrimitive.RadioGroup {...props} />;
}

function MenubarSub({
  ...props
}) {
  return <MenubarPrimitive.Sub data-slot="menubar-sub" {...props} />;
}

const Menubar = React.forwardRef(({ className, ...props }, ref) => (
  <MenubarPrimitive.Root
    ref={ref}
    className={cn(
      "flex h-9 items-center space-x-1 rounded-md border bg-background p-1 shadow-sm",
      className
    )}
    {...props} />
))
Menubar.displayName = MenubarPrimitive.Root.displayName

const MenubarTrigger = React.forwardRef(({ className, ...props }, ref) => (
  <MenubarPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-3 py-1 text-sm font-medium outline-none focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
      className
    )}
    {...props} />
))
MenubarTrigger.displayName = MenubarPrimitive.Trigger.displayName

const MenubarSubTrigger = React.forwardRef(({ className, inset, children, ...props }, ref) => (
  <MenubarPrimitive.SubTrigger
    ref={ref}
    className={cn(
      "flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[state=open]:bg-accent data-[state=open]:text-accent-foreground",
      inset && "pl-8",
      className
    )}
    {...props}>
    {children}
    <ChevronRight className="ml-auto h-4 w-4" />
  </MenubarPrimitive.SubTrigger>
))
MenubarSubTrigger.displayName = MenubarPrimitive.SubTrigger.displayName

const MenubarSubContent = React.forwardRef(({ className, ...props }, ref) => (
  <MenubarPrimitive.SubContent
    ref={ref}
    className={cn(
      "z-50 min-w-[8rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-lg data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-menubar-content-transform-origin]",
      className
    )}
    {...props} />
))
MenubarSubContent.displayName = MenubarPrimitive.SubContent.displayName

const MenubarContent = React.forwardRef((
  { className, align = "start", alignOffset = -4, sideOffset = 8, ...props },
  ref
) => (
  <MenubarPrimitive.Portal>
    <MenubarPrimitive.Content
      ref={ref}
      align={align}
      alignOffset={alignOffset}
      sideOffset={sideOffset}
      className={cn(
        "z-50 min-w-[12rem] overflow-hidden rounded-md border bg-popover p-1 text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-menubar-content-transform-origin]",
        className
      )}
      {...props} />
  </MenubarPrimitive.Portal>
))
MenubarContent.displayName = MenubarPrimitive.Content.displayName

const MenubarItem = React.forwardRef(({ className, inset, ...props }, ref) => (
  <MenubarPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm px-2 py-1.5 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      inset && "pl-8",
      className
    )}
    {...props} />
))
MenubarItem.displayName = MenubarPrimitive.Item.displayName

const MenubarCheckboxItem = React.forwardRef(({ className, children, checked, ...props }, ref) => (
  <MenubarPrimitive.CheckboxItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    checked={checked}
    {...props}>
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <MenubarPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </MenubarPrimitive.ItemIndicator>
    </span>
    {children}
  </MenubarPrimitive.CheckboxItem>
))
MenubarCheckboxItem.displayName = MenubarPrimitive.CheckboxItem.displayName

const MenubarRadioItem = React.forwardRef(({ className, children, ...props }, ref) => (
  <MenubarPrimitive.RadioItem
    ref={ref}
    className={cn(
      "relative flex cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}>
    <span className="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
      <MenubarPrimitive.ItemIndicator>
        <Circle className="h-4 w-4 fill-current" />
      </MenubarPrimitive.ItemIndicator>
    </span>
    {children}
  </MenubarPrimitive.RadioItem>
))
MenubarRadioItem.displayName = MenubarPrimitive.RadioItem.displayName

const MenubarLabel = React.forwardRef(({ className, inset, ...props }, ref) => (
  <MenubarPrimitive.Label
    ref={ref}
    className={cn("px-2 py-1.5 text-sm font-semibold", inset && "pl-8", className)}
    {...props} />
))
MenubarLabel.displayName = MenubarPrimitive.Label.displayName

const MenubarSeparator = React.forwardRef(({ className, ...props }, ref) => (
  <MenubarPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-muted", className)}
    {...props} />
))
MenubarSeparator.displayName = MenubarPrimitive.Separator.displayName

const MenubarShortcut = ({
  className,
  ...props
}) => {
  return (
    <span
      className={cn("ml-auto text-xs tracking-widest text-muted-foreground", className)}
      {...props} />
  );
}
MenubarShortcut.displayname = "MenubarShortcut"

export {
  Menubar,
  MenubarMenu,
  MenubarTrigger,
  MenubarContent,
  MenubarItem,
  MenubarSeparator,
  MenubarLabel,
  MenubarCheckboxItem,
  MenubarRadioGroup,
  MenubarRadioItem,
  MenubarPortal,
  MenubarSubContent,
  MenubarSubTrigger,
  MenubarGroup,
  MenubarSub,
  MenubarShortcut,
}

===== FILE: frontend/src/components/ui/navigation-menu.jsx =====
import * as React from "react"
import * as NavigationMenuPrimitive from "@radix-ui/react-navigation-menu"
import { cva } from "class-variance-authority"
import { ChevronDown } from "lucide-react"

import { cn } from "@/lib/utils"

const NavigationMenu = React.forwardRef(({ className, children, ...props }, ref) => (
  <NavigationMenuPrimitive.Root
    ref={ref}
    className={cn(
      "relative z-10 flex max-w-max flex-1 items-center justify-center",
      className
    )}
    {...props}>
    {children}
    <NavigationMenuViewport />
  </NavigationMenuPrimitive.Root>
))
NavigationMenu.displayName = NavigationMenuPrimitive.Root.displayName

const NavigationMenuList = React.forwardRef(({ className, ...props }, ref) => (
  <NavigationMenuPrimitive.List
    ref={ref}
    className={cn(
      "group flex flex-1 list-none items-center justify-center space-x-1",
      className
    )}
    {...props} />
))
NavigationMenuList.displayName = NavigationMenuPrimitive.List.displayName

const NavigationMenuItem = NavigationMenuPrimitive.Item

const navigationMenuTriggerStyle = cva(
  "group inline-flex h-9 w-max items-center justify-center rounded-md bg-background px-4 py-2 text-sm font-medium transition-colors hover:bg-accent hover:text-accent-foreground focus:bg-accent focus:text-accent-foreground focus:outline-none disabled:pointer-events-none disabled:opacity-50 data-[state=open]:text-accent-foreground data-[state=open]:bg-accent/50 data-[state=open]:hover:bg-accent data-[state=open]:focus:bg-accent"
)

const NavigationMenuTrigger = React.forwardRef(({ className, children, ...props }, ref) => (
  <NavigationMenuPrimitive.Trigger
    ref={ref}
    className={cn(navigationMenuTriggerStyle(), "group", className)}
    {...props}>
    {children}{" "}
    <ChevronDown
      className="relative top-[1px] ml-1 h-3 w-3 transition duration-300 group-data-[state=open]:rotate-180"
      aria-hidden="true" />
  </NavigationMenuPrimitive.Trigger>
))
NavigationMenuTrigger.displayName = NavigationMenuPrimitive.Trigger.displayName

const NavigationMenuContent = React.forwardRef(({ className, ...props }, ref) => (
  <NavigationMenuPrimitive.Content
    ref={ref}
    className={cn(
      "left-0 top-0 w-full data-[motion^=from-]:animate-in data-[motion^=to-]:animate-out data-[motion^=from-]:fade-in data-[motion^=to-]:fade-out data-[motion=from-end]:slide-in-from-right-52 data-[motion=from-start]:slide-in-from-left-52 data-[motion=to-end]:slide-out-to-right-52 data-[motion=to-start]:slide-out-to-left-52 md:absolute md:w-auto ",
      className
    )}
    {...props} />
))
NavigationMenuContent.displayName = NavigationMenuPrimitive.Content.displayName

const NavigationMenuLink = NavigationMenuPrimitive.Link

const NavigationMenuViewport = React.forwardRef(({ className, ...props }, ref) => (
  <div className={cn("absolute left-0 top-full flex justify-center")}>
    <NavigationMenuPrimitive.Viewport
      className={cn(
        "origin-top-center relative mt-1.5 h-[var(--radix-navigation-menu-viewport-height)] w-full overflow-hidden rounded-md border bg-popover text-popover-foreground shadow data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-90 md:w-[var(--radix-navigation-menu-viewport-width)]",
        className
      )}
      ref={ref}
      {...props} />
  </div>
))
NavigationMenuViewport.displayName =
  NavigationMenuPrimitive.Viewport.displayName

const NavigationMenuIndicator = React.forwardRef(({ className, ...props }, ref) => (
  <NavigationMenuPrimitive.Indicator
    ref={ref}
    className={cn(
      "top-full z-[1] flex h-1.5 items-end justify-center overflow-hidden data-[state=visible]:animate-in data-[state=hidden]:animate-out data-[state=hidden]:fade-out data-[state=visible]:fade-in",
      className
    )}
    {...props}>
    <div
      className="relative top-[60%] h-2 w-2 rotate-45 rounded-tl-sm bg-border shadow-md" />
  </NavigationMenuPrimitive.Indicator>
))
NavigationMenuIndicator.displayName =
  NavigationMenuPrimitive.Indicator.displayName

export {
  navigationMenuTriggerStyle,
  NavigationMenu,
  NavigationMenuList,
  NavigationMenuItem,
  NavigationMenuContent,
  NavigationMenuTrigger,
  NavigationMenuLink,
  NavigationMenuIndicator,
  NavigationMenuViewport,
}

===== FILE: frontend/src/components/ui/pagination.jsx =====
import * as React from "react"
import { ChevronLeft, ChevronRight, MoreHorizontal } from "lucide-react"

import { cn } from "@/lib/utils"
import { buttonVariants } from "@/components/ui/button";

const Pagination = ({
  className,
  ...props
}) => (
  <nav
    role="navigation"
    aria-label="pagination"
    className={cn("mx-auto flex w-full justify-center", className)}
    {...props} />
)
Pagination.displayName = "Pagination"

const PaginationContent = React.forwardRef(({ className, ...props }, ref) => (
  <ul
    ref={ref}
    className={cn("flex flex-row items-center gap-1", className)}
    {...props} />
))
PaginationContent.displayName = "PaginationContent"

const PaginationItem = React.forwardRef(({ className, ...props }, ref) => (
  <li ref={ref} className={cn("", className)} {...props} />
))
PaginationItem.displayName = "PaginationItem"

const PaginationLink = ({
  className,
  isActive,
  size = "icon",
  ...props
}) => (
  <a
    aria-current={isActive ? "page" : undefined}
    className={cn(buttonVariants({
      variant: isActive ? "outline" : "ghost",
      size,
    }), className)}
    {...props} />
)
PaginationLink.displayName = "PaginationLink"

const PaginationPrevious = ({
  className,
  ...props
}) => (
  <PaginationLink
    aria-label="Go to previous page"
    size="default"
    className={cn("gap-1 pl-2.5", className)}
    {...props}>
    <ChevronLeft className="h-4 w-4" />
    <span>Previous</span>
  </PaginationLink>
)
PaginationPrevious.displayName = "PaginationPrevious"

const PaginationNext = ({
  className,
  ...props
}) => (
  <PaginationLink
    aria-label="Go to next page"
    size="default"
    className={cn("gap-1 pr-2.5", className)}
    {...props}>
    <span>Next</span>
    <ChevronRight className="h-4 w-4" />
  </PaginationLink>
)
PaginationNext.displayName = "PaginationNext"

const PaginationEllipsis = ({
  className,
  ...props
}) => (
  <span
    aria-hidden
    className={cn("flex h-9 w-9 items-center justify-center", className)}
    {...props}>
    <MoreHorizontal className="h-4 w-4" />
    <span className="sr-only">More pages</span>
  </span>
)
PaginationEllipsis.displayName = "PaginationEllipsis"

export {
  Pagination,
  PaginationContent,
  PaginationLink,
  PaginationItem,
  PaginationPrevious,
  PaginationNext,
  PaginationEllipsis,
}

===== FILE: frontend/src/components/ui/popover.jsx =====
import * as React from "react"
import * as PopoverPrimitive from "@radix-ui/react-popover"

import { cn } from "@/lib/utils"

const Popover = PopoverPrimitive.Root

const PopoverTrigger = PopoverPrimitive.Trigger

const PopoverAnchor = PopoverPrimitive.Anchor

const PopoverContent = React.forwardRef(({ className, align = "center", sideOffset = 4, ...props }, ref) => (
  <PopoverPrimitive.Portal>
    <PopoverPrimitive.Content
      ref={ref}
      align={align}
      sideOffset={sideOffset}
      className={cn(
        "z-50 w-72 rounded-md border bg-popover p-4 text-popover-foreground shadow-md outline-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-popover-content-transform-origin]",
        className
      )}
      {...props} />
  </PopoverPrimitive.Portal>
))
PopoverContent.displayName = PopoverPrimitive.Content.displayName

export { Popover, PopoverTrigger, PopoverContent, PopoverAnchor }

===== FILE: frontend/src/components/ui/progress.jsx =====
import * as React from "react"
import * as ProgressPrimitive from "@radix-ui/react-progress"

import { cn } from "@/lib/utils"

const Progress = React.forwardRef(({ className, value, ...props }, ref) => (
  <ProgressPrimitive.Root
    ref={ref}
    className={cn(
      "relative h-2 w-full overflow-hidden rounded-full bg-primary/20",
      className
    )}
    {...props}>
    <ProgressPrimitive.Indicator
      className="h-full w-full flex-1 bg-primary transition-all"
      style={{ transform: `translateX(-${100 - (value || 0)}%)` }} />
  </ProgressPrimitive.Root>
))
Progress.displayName = ProgressPrimitive.Root.displayName

export { Progress }

===== FILE: frontend/src/components/ui/radio-group.jsx =====
import * as React from "react"
import * as RadioGroupPrimitive from "@radix-ui/react-radio-group"
import { Circle } from "lucide-react"

import { cn } from "@/lib/utils"

const RadioGroup = React.forwardRef(({ className, ...props }, ref) => {
  return (<RadioGroupPrimitive.Root className={cn("grid gap-2", className)} {...props} ref={ref} />);
})
RadioGroup.displayName = RadioGroupPrimitive.Root.displayName

const RadioGroupItem = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <RadioGroupPrimitive.Item
      ref={ref}
      className={cn(
        "aspect-square h-4 w-4 rounded-full border border-primary text-primary shadow focus:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50",
        className
      )}
      {...props}>
      <RadioGroupPrimitive.Indicator className="flex items-center justify-center">
        <Circle className="h-3.5 w-3.5 fill-primary" />
      </RadioGroupPrimitive.Indicator>
    </RadioGroupPrimitive.Item>
  );
})
RadioGroupItem.displayName = RadioGroupPrimitive.Item.displayName

export { RadioGroup, RadioGroupItem }

===== FILE: frontend/src/components/ui/resizable.jsx =====
import { GripVertical } from "lucide-react"
import * as ResizablePrimitive from "react-resizable-panels"

import { cn } from "@/lib/utils"

const ResizablePanelGroup = ({
  className,
  ...props
}) => (
  <ResizablePrimitive.PanelGroup
    className={cn(
      "flex h-full w-full data-[panel-group-direction=vertical]:flex-col",
      className
    )}
    {...props} />
)

const ResizablePanel = ResizablePrimitive.Panel

const ResizableHandle = ({
  withHandle,
  className,
  ...props
}) => (
  <ResizablePrimitive.PanelResizeHandle
    className={cn(
      "relative flex w-px items-center justify-center bg-border after:absolute after:inset-y-0 after:left-1/2 after:w-1 after:-translate-x-1/2 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring focus-visible:ring-offset-1 data-[panel-group-direction=vertical]:h-px data-[panel-group-direction=vertical]:w-full data-[panel-group-direction=vertical]:after:left-0 data-[panel-group-direction=vertical]:after:h-1 data-[panel-group-direction=vertical]:after:w-full data-[panel-group-direction=vertical]:after:-translate-y-1/2 data-[panel-group-direction=vertical]:after:translate-x-0 [&[data-panel-group-direction=vertical]>div]:rotate-90",
      className
    )}
    {...props}>
    {withHandle && (
      <div
        className="z-10 flex h-4 w-3 items-center justify-center rounded-sm border bg-border">
        <GripVertical className="h-2.5 w-2.5" />
      </div>
    )}
  </ResizablePrimitive.PanelResizeHandle>
)

export { ResizablePanelGroup, ResizablePanel, ResizableHandle }

===== FILE: frontend/src/components/ui/scroll-area.jsx =====
import * as React from "react"
import * as ScrollAreaPrimitive from "@radix-ui/react-scroll-area"

import { cn } from "@/lib/utils"

const ScrollArea = React.forwardRef(({ className, children, ...props }, ref) => (
  <ScrollAreaPrimitive.Root
    ref={ref}
    className={cn("relative overflow-hidden", className)}
    {...props}>
    <ScrollAreaPrimitive.Viewport className="h-full w-full rounded-[inherit]">
      {children}
    </ScrollAreaPrimitive.Viewport>
    <ScrollBar />
    <ScrollAreaPrimitive.Corner />
  </ScrollAreaPrimitive.Root>
))
ScrollArea.displayName = ScrollAreaPrimitive.Root.displayName

const ScrollBar = React.forwardRef(({ className, orientation = "vertical", ...props }, ref) => (
  <ScrollAreaPrimitive.ScrollAreaScrollbar
    ref={ref}
    orientation={orientation}
    className={cn(
      "flex touch-none select-none transition-colors",
      orientation === "vertical" &&
        "h-full w-2.5 border-l border-l-transparent p-[1px]",
      orientation === "horizontal" &&
        "h-2.5 flex-col border-t border-t-transparent p-[1px]",
      className
    )}
    {...props}>
    <ScrollAreaPrimitive.ScrollAreaThumb className="relative flex-1 rounded-full bg-border" />
  </ScrollAreaPrimitive.ScrollAreaScrollbar>
))
ScrollBar.displayName = ScrollAreaPrimitive.ScrollAreaScrollbar.displayName

export { ScrollArea, ScrollBar }

===== FILE: frontend/src/components/ui/select.jsx =====
import * as React from "react"
import * as SelectPrimitive from "@radix-ui/react-select"
import { Check, ChevronDown, ChevronUp } from "lucide-react"

import { cn } from "@/lib/utils"

const Select = SelectPrimitive.Root

const SelectGroup = SelectPrimitive.Group

const SelectValue = SelectPrimitive.Value

const SelectTrigger = React.forwardRef(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Trigger
    ref={ref}
    className={cn(
      "flex h-9 w-full items-center justify-between whitespace-nowrap rounded-md border border-input bg-transparent px-3 py-2 text-sm shadow-sm ring-offset-background data-[placeholder]:text-muted-foreground focus:outline-none focus:ring-1 focus:ring-ring disabled:cursor-not-allowed disabled:opacity-50 [&>span]:line-clamp-1",
      className
    )}
    {...props}>
    {children}
    <SelectPrimitive.Icon asChild>
      <ChevronDown className="h-4 w-4 opacity-50" />
    </SelectPrimitive.Icon>
  </SelectPrimitive.Trigger>
))
SelectTrigger.displayName = SelectPrimitive.Trigger.displayName

const SelectScrollUpButton = React.forwardRef(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollUpButton
    ref={ref}
    className={cn("flex cursor-default items-center justify-center py-1", className)}
    {...props}>
    <ChevronUp className="h-4 w-4" />
  </SelectPrimitive.ScrollUpButton>
))
SelectScrollUpButton.displayName = SelectPrimitive.ScrollUpButton.displayName

const SelectScrollDownButton = React.forwardRef(({ className, ...props }, ref) => (
  <SelectPrimitive.ScrollDownButton
    ref={ref}
    className={cn("flex cursor-default items-center justify-center py-1", className)}
    {...props}>
    <ChevronDown className="h-4 w-4" />
  </SelectPrimitive.ScrollDownButton>
))
SelectScrollDownButton.displayName =
  SelectPrimitive.ScrollDownButton.displayName

const SelectContent = React.forwardRef(({ className, children, position = "popper", ...props }, ref) => (
  <SelectPrimitive.Portal>
    <SelectPrimitive.Content
      ref={ref}
      className={cn(
        "relative z-50 max-h-[--radix-select-content-available-height] min-w-[8rem] overflow-y-auto overflow-x-hidden rounded-md border bg-popover text-popover-foreground shadow-md data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-select-content-transform-origin]",
        position === "popper" &&
          "data-[side=bottom]:translate-y-1 data-[side=left]:-translate-x-1 data-[side=right]:translate-x-1 data-[side=top]:-translate-y-1",
        className
      )}
      position={position}
      {...props}>
      <SelectScrollUpButton />
      <SelectPrimitive.Viewport
        className={cn("p-1", position === "popper" &&
          "h-[var(--radix-select-trigger-height)] w-full min-w-[var(--radix-select-trigger-width)]")}>
        {children}
      </SelectPrimitive.Viewport>
      <SelectScrollDownButton />
    </SelectPrimitive.Content>
  </SelectPrimitive.Portal>
))
SelectContent.displayName = SelectPrimitive.Content.displayName

const SelectLabel = React.forwardRef(({ className, ...props }, ref) => (
  <SelectPrimitive.Label
    ref={ref}
    className={cn("px-2 py-1.5 text-sm font-semibold", className)}
    {...props} />
))
SelectLabel.displayName = SelectPrimitive.Label.displayName

const SelectItem = React.forwardRef(({ className, children, ...props }, ref) => (
  <SelectPrimitive.Item
    ref={ref}
    className={cn(
      "relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-2 pr-8 text-sm outline-none focus:bg-accent focus:text-accent-foreground data-[disabled]:pointer-events-none data-[disabled]:opacity-50",
      className
    )}
    {...props}>
    <span className="absolute right-2 flex h-3.5 w-3.5 items-center justify-center">
      <SelectPrimitive.ItemIndicator>
        <Check className="h-4 w-4" />
      </SelectPrimitive.ItemIndicator>
    </span>
    <SelectPrimitive.ItemText>{children}</SelectPrimitive.ItemText>
  </SelectPrimitive.Item>
))
SelectItem.displayName = SelectPrimitive.Item.displayName

const SelectSeparator = React.forwardRef(({ className, ...props }, ref) => (
  <SelectPrimitive.Separator
    ref={ref}
    className={cn("-mx-1 my-1 h-px bg-muted", className)}
    {...props} />
))
SelectSeparator.displayName = SelectPrimitive.Separator.displayName

export {
  Select,
  SelectGroup,
  SelectValue,
  SelectTrigger,
  SelectContent,
  SelectLabel,
  SelectItem,
  SelectSeparator,
  SelectScrollUpButton,
  SelectScrollDownButton,
}

===== FILE: frontend/src/components/ui/separator.jsx =====
import * as React from "react"
import * as SeparatorPrimitive from "@radix-ui/react-separator"

import { cn } from "@/lib/utils"

const Separator = React.forwardRef((
  { className, orientation = "horizontal", decorative = true, ...props },
  ref
) => (
  <SeparatorPrimitive.Root
    ref={ref}
    decorative={decorative}
    orientation={orientation}
    className={cn(
      "shrink-0 bg-border",
      orientation === "horizontal" ? "h-[1px] w-full" : "h-full w-[1px]",
      className
    )}
    {...props} />
))
Separator.displayName = SeparatorPrimitive.Root.displayName

export { Separator }

===== FILE: frontend/src/components/ui/sheet.jsx =====
import * as React from "react"
import * as SheetPrimitive from "@radix-ui/react-dialog"
import { cva } from "class-variance-authority";
import { X } from "lucide-react"

import { cn } from "@/lib/utils"

const Sheet = SheetPrimitive.Root

const SheetTrigger = SheetPrimitive.Trigger

const SheetClose = SheetPrimitive.Close

const SheetPortal = SheetPrimitive.Portal

const SheetOverlay = React.forwardRef(({ className, ...props }, ref) => (
  <SheetPrimitive.Overlay
    className={cn(
      "fixed inset-0 z-50 bg-black/80  data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0",
      className
    )}
    {...props}
    ref={ref} />
))
SheetOverlay.displayName = SheetPrimitive.Overlay.displayName

const sheetVariants = cva(
  "fixed z-50 gap-4 bg-background p-6 shadow-lg transition ease-in-out data-[state=closed]:duration-300 data-[state=open]:duration-500 data-[state=open]:animate-in data-[state=closed]:animate-out",
  {
    variants: {
      side: {
        top: "inset-x-0 top-0 border-b data-[state=closed]:slide-out-to-top data-[state=open]:slide-in-from-top",
        bottom:
          "inset-x-0 bottom-0 border-t data-[state=closed]:slide-out-to-bottom data-[state=open]:slide-in-from-bottom",
        left: "inset-y-0 left-0 h-full w-3/4 border-r data-[state=closed]:slide-out-to-left data-[state=open]:slide-in-from-left sm:max-w-sm",
        right:
          "inset-y-0 right-0 h-full w-3/4 border-l data-[state=closed]:slide-out-to-right data-[state=open]:slide-in-from-right sm:max-w-sm",
      },
    },
    defaultVariants: {
      side: "right",
    },
  }
)

const SheetContent = React.forwardRef(({ side = "right", className, children, ...props }, ref) => (
  <SheetPortal>
    <SheetOverlay />
    <SheetPrimitive.Content ref={ref} className={cn(sheetVariants({ side }), className)} {...props}>
      <SheetPrimitive.Close
        className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-secondary">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </SheetPrimitive.Close>
      {children}
    </SheetPrimitive.Content>
  </SheetPortal>
))
SheetContent.displayName = SheetPrimitive.Content.displayName

const SheetHeader = ({
  className,
  ...props
}) => (
  <div
    className={cn("flex flex-col space-y-2 text-center sm:text-left", className)}
    {...props} />
)
SheetHeader.displayName = "SheetHeader"

const SheetFooter = ({
  className,
  ...props
}) => (
  <div
    className={cn("flex flex-col-reverse sm:flex-row sm:justify-end sm:space-x-2", className)}
    {...props} />
)
SheetFooter.displayName = "SheetFooter"

const SheetTitle = React.forwardRef(({ className, ...props }, ref) => (
  <SheetPrimitive.Title
    ref={ref}
    className={cn("text-lg font-semibold text-foreground", className)}
    {...props} />
))
SheetTitle.displayName = SheetPrimitive.Title.displayName

const SheetDescription = React.forwardRef(({ className, ...props }, ref) => (
  <SheetPrimitive.Description
    ref={ref}
    className={cn("text-sm text-muted-foreground", className)}
    {...props} />
))
SheetDescription.displayName = SheetPrimitive.Description.displayName

export {
  Sheet,
  SheetPortal,
  SheetOverlay,
  SheetTrigger,
  SheetClose,
  SheetContent,
  SheetHeader,
  SheetFooter,
  SheetTitle,
  SheetDescription,
}

===== FILE: frontend/src/components/ui/skeleton.jsx =====
import { cn } from "@/lib/utils"

function Skeleton({
  className,
  ...props
}) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-primary/10", className)}
      {...props} />
  );
}

export { Skeleton }

===== FILE: frontend/src/components/ui/slider.jsx =====
import * as React from "react"
import * as SliderPrimitive from "@radix-ui/react-slider"

import { cn } from "@/lib/utils"

const Slider = React.forwardRef(({ className, ...props }, ref) => (
  <SliderPrimitive.Root
    ref={ref}
    className={cn("relative flex w-full touch-none select-none items-center", className)}
    {...props}>
    <SliderPrimitive.Track
      className="relative h-1.5 w-full grow overflow-hidden rounded-full bg-primary/20">
      <SliderPrimitive.Range className="absolute h-full bg-primary" />
    </SliderPrimitive.Track>
    <SliderPrimitive.Thumb
      className="block h-4 w-4 rounded-full border border-primary/50 bg-background shadow transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50" />
  </SliderPrimitive.Root>
))
Slider.displayName = SliderPrimitive.Root.displayName

export { Slider }

===== FILE: frontend/src/components/ui/sonner.jsx =====
import { useTheme } from "next-themes"
import { Toaster as Sonner, toast } from "sonner"

const Toaster = ({
  ...props
}) => {
  const { theme = "system" } = useTheme()

  return (
    <Sonner
      theme={theme}
      className="toaster group"
      toastOptions={{
        classNames: {
          toast:
            "group toast group-[.toaster]:bg-background group-[.toaster]:text-foreground group-[.toaster]:border-border group-[.toaster]:shadow-lg",
          description: "group-[.toast]:text-muted-foreground",
          actionButton:
            "group-[.toast]:bg-primary group-[.toast]:text-primary-foreground",
          cancelButton:
            "group-[.toast]:bg-muted group-[.toast]:text-muted-foreground",
        },
      }}
      {...props} />
  );
}

export { Toaster, toast }

===== FILE: frontend/src/components/ui/switch.jsx =====
import * as React from "react"
import * as SwitchPrimitives from "@radix-ui/react-switch"

import { cn } from "@/lib/utils"

const Switch = React.forwardRef(({ className, ...props }, ref) => (
  <SwitchPrimitives.Root
    className={cn(
      "peer inline-flex h-5 w-9 shrink-0 cursor-pointer items-center rounded-full border-2 border-transparent shadow-sm transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 focus-visible:ring-offset-background disabled:cursor-not-allowed disabled:opacity-50 data-[state=checked]:bg-primary data-[state=unchecked]:bg-input",
      className
    )}
    {...props}
    ref={ref}>
    <SwitchPrimitives.Thumb
      className={cn(
        "pointer-events-none block h-4 w-4 rounded-full bg-background shadow-lg ring-0 transition-transform data-[state=checked]:translate-x-4 data-[state=unchecked]:translate-x-0"
      )} />
  </SwitchPrimitives.Root>
))
Switch.displayName = SwitchPrimitives.Root.displayName

export { Switch }

===== FILE: frontend/src/components/ui/table.jsx =====
import * as React from "react"

import { cn } from "@/lib/utils"

const Table = React.forwardRef(({ className, ...props }, ref) => (
  <div className="relative w-full overflow-auto">
    <table
      ref={ref}
      className={cn("w-full caption-bottom text-sm", className)}
      {...props} />
  </div>
))
Table.displayName = "Table"

const TableHeader = React.forwardRef(({ className, ...props }, ref) => (
  <thead ref={ref} className={cn("[&_tr]:border-b", className)} {...props} />
))
TableHeader.displayName = "TableHeader"

const TableBody = React.forwardRef(({ className, ...props }, ref) => (
  <tbody
    ref={ref}
    className={cn("[&_tr:last-child]:border-0", className)}
    {...props} />
))
TableBody.displayName = "TableBody"

const TableFooter = React.forwardRef(({ className, ...props }, ref) => (
  <tfoot
    ref={ref}
    className={cn("border-t bg-muted/50 font-medium [&>tr]:last:border-b-0", className)}
    {...props} />
))
TableFooter.displayName = "TableFooter"

const TableRow = React.forwardRef(({ className, ...props }, ref) => (
  <tr
    ref={ref}
    className={cn(
      "border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted",
      className
    )}
    {...props} />
))
TableRow.displayName = "TableRow"

const TableHead = React.forwardRef(({ className, ...props }, ref) => (
  <th
    ref={ref}
    className={cn(
      "h-10 px-2 text-left align-middle font-medium text-muted-foreground [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
      className
    )}
    {...props} />
))
TableHead.displayName = "TableHead"

const TableCell = React.forwardRef(({ className, ...props }, ref) => (
  <td
    ref={ref}
    className={cn(
      "p-2 align-middle [&:has([role=checkbox])]:pr-0 [&>[role=checkbox]]:translate-y-[2px]",
      className
    )}
    {...props} />
))
TableCell.displayName = "TableCell"

const TableCaption = React.forwardRef(({ className, ...props }, ref) => (
  <caption
    ref={ref}
    className={cn("mt-4 text-sm text-muted-foreground", className)}
    {...props} />
))
TableCaption.displayName = "TableCaption"

export {
  Table,
  TableHeader,
  TableBody,
  TableFooter,
  TableHead,
  TableRow,
  TableCell,
  TableCaption,
}

===== FILE: frontend/src/components/ui/tabs.jsx =====
import * as React from "react"
import * as TabsPrimitive from "@radix-ui/react-tabs"

import { cn } from "@/lib/utils"

const Tabs = TabsPrimitive.Root

const TabsList = React.forwardRef(({ className, ...props }, ref) => (
  <TabsPrimitive.List
    ref={ref}
    className={cn(
      "inline-flex h-9 items-center justify-center rounded-lg bg-muted p-1 text-muted-foreground",
      className
    )}
    {...props} />
))
TabsList.displayName = TabsPrimitive.List.displayName

const TabsTrigger = React.forwardRef(({ className, ...props }, ref) => (
  <TabsPrimitive.Trigger
    ref={ref}
    className={cn(
      "inline-flex items-center justify-center whitespace-nowrap rounded-md px-3 py-1 text-sm font-medium ring-offset-background transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 data-[state=active]:bg-background data-[state=active]:text-foreground data-[state=active]:shadow",
      className
    )}
    {...props} />
))
TabsTrigger.displayName = TabsPrimitive.Trigger.displayName

const TabsContent = React.forwardRef(({ className, ...props }, ref) => (
  <TabsPrimitive.Content
    ref={ref}
    className={cn(
      "mt-2 ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2",
      className
    )}
    {...props} />
))
TabsContent.displayName = TabsPrimitive.Content.displayName

export { Tabs, TabsList, TabsTrigger, TabsContent }

===== FILE: frontend/src/components/ui/textarea.jsx =====
import * as React from "react"

import { cn } from "@/lib/utils"

const Textarea = React.forwardRef(({ className, ...props }, ref) => {
  return (
    <textarea
      className={cn(
        "flex min-h-[60px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-base shadow-sm placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50 md:text-sm",
        className
      )}
      ref={ref}
      {...props} />
  );
})
Textarea.displayName = "Textarea"

export { Textarea }

===== FILE: frontend/src/components/ui/toast.jsx =====
import * as React from "react"
import * as ToastPrimitives from "@radix-ui/react-toast"
import { cva } from "class-variance-authority";
import { X } from "lucide-react"

import { cn } from "@/lib/utils"

const ToastProvider = ToastPrimitives.Provider

const ToastViewport = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Viewport
    ref={ref}
    className={cn(
      "fixed top-0 z-[100] flex max-h-screen w-full flex-col-reverse p-4 sm:bottom-0 sm:right-0 sm:top-auto sm:flex-col md:max-w-[420px]",
      className
    )}
    {...props} />
))
ToastViewport.displayName = ToastPrimitives.Viewport.displayName

const toastVariants = cva(
  "group pointer-events-auto relative flex w-full items-center justify-between space-x-2 overflow-hidden rounded-md border p-4 pr-6 shadow-lg transition-all data-[swipe=cancel]:translate-x-0 data-[swipe=end]:translate-x-[var(--radix-toast-swipe-end-x)] data-[swipe=move]:translate-x-[var(--radix-toast-swipe-move-x)] data-[swipe=move]:transition-none data-[state=open]:animate-in data-[state=closed]:animate-out data-[swipe=end]:animate-out data-[state=closed]:fade-out-80 data-[state=closed]:slide-out-to-right-full data-[state=open]:slide-in-from-top-full data-[state=open]:sm:slide-in-from-bottom-full",
  {
    variants: {
      variant: {
        default: "border bg-background text-foreground",
        destructive:
          "destructive group border-destructive bg-destructive text-destructive-foreground",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  }
)

const Toast = React.forwardRef(({ className, variant, ...props }, ref) => {
  return (
    <ToastPrimitives.Root
      ref={ref}
      className={cn(toastVariants({ variant }), className)}
      {...props} />
  );
})
Toast.displayName = ToastPrimitives.Root.displayName

const ToastAction = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Action
    ref={ref}
    className={cn(
      "inline-flex h-8 shrink-0 items-center justify-center rounded-md border bg-transparent px-3 text-sm font-medium transition-colors hover:bg-secondary focus:outline-none focus:ring-1 focus:ring-ring disabled:pointer-events-none disabled:opacity-50 group-[.destructive]:border-muted/40 group-[.destructive]:hover:border-destructive/30 group-[.destructive]:hover:bg-destructive group-[.destructive]:hover:text-destructive-foreground group-[.destructive]:focus:ring-destructive",
      className
    )}
    {...props} />
))
ToastAction.displayName = ToastPrimitives.Action.displayName

const ToastClose = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Close
    ref={ref}
    className={cn(
      "absolute right-1 top-1 rounded-md p-1 text-foreground/50 opacity-0 transition-opacity hover:text-foreground focus:opacity-100 focus:outline-none focus:ring-1 group-hover:opacity-100 group-[.destructive]:text-red-300 group-[.destructive]:hover:text-red-50 group-[.destructive]:focus:ring-red-400 group-[.destructive]:focus:ring-offset-red-600",
      className
    )}
    toast-close=""
    {...props}>
    <X className="h-4 w-4" />
  </ToastPrimitives.Close>
))
ToastClose.displayName = ToastPrimitives.Close.displayName

const ToastTitle = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Title
    ref={ref}
    className={cn("text-sm font-semibold [&+div]:text-xs", className)}
    {...props} />
))
ToastTitle.displayName = ToastPrimitives.Title.displayName

const ToastDescription = React.forwardRef(({ className, ...props }, ref) => (
  <ToastPrimitives.Description ref={ref} className={cn("text-sm opacity-90", className)} {...props} />
))
ToastDescription.displayName = ToastPrimitives.Description.displayName

export { ToastProvider, ToastViewport, Toast, ToastTitle, ToastDescription, ToastClose, ToastAction };

===== FILE: frontend/src/components/ui/toaster.jsx =====
import { useToast } from "@/hooks/use-toast"
import {
  Toast,
  ToastClose,
  ToastDescription,
  ToastProvider,
  ToastTitle,
  ToastViewport,
} from "@/components/ui/toast"

export function Toaster() {
  const { toasts } = useToast()

  return (
    <ToastProvider>
      {toasts.map(function ({ id, title, description, action, ...props }) {
        return (
          <Toast key={id} {...props}>
            <div className="grid gap-1">
              {title && <ToastTitle>{title}</ToastTitle>}
              {description && (
                <ToastDescription>{description}</ToastDescription>
              )}
            </div>
            {action}
            <ToastClose />
          </Toast>
        );
      })}
      <ToastViewport />
    </ToastProvider>
  );
}

===== FILE: frontend/src/components/ui/toggle-group.jsx =====
import * as React from "react"
import * as ToggleGroupPrimitive from "@radix-ui/react-toggle-group"

import { cn } from "@/lib/utils"
import { toggleVariants } from "@/components/ui/toggle"

const ToggleGroupContext = React.createContext({
  size: "default",
  variant: "default",
})

const ToggleGroup = React.forwardRef(({ className, variant, size, children, ...props }, ref) => (
  <ToggleGroupPrimitive.Root
    ref={ref}
    className={cn("flex items-center justify-center gap-1", className)}
    {...props}>
    <ToggleGroupContext.Provider value={{ variant, size }}>
      {children}
    </ToggleGroupContext.Provider>
  </ToggleGroupPrimitive.Root>
))

ToggleGroup.displayName = ToggleGroupPrimitive.Root.displayName

const ToggleGroupItem = React.forwardRef(({ className, children, variant, size, ...props }, ref) => {
  const context = React.useContext(ToggleGroupContext)

  return (
    <ToggleGroupPrimitive.Item
      ref={ref}
      className={cn(toggleVariants({
        variant: context.variant || variant,
        size: context.size || size,
      }), className)}
      {...props}>
      {children}
    </ToggleGroupPrimitive.Item>
  );
})

ToggleGroupItem.displayName = ToggleGroupPrimitive.Item.displayName

export { ToggleGroup, ToggleGroupItem }

===== FILE: frontend/src/components/ui/toggle.jsx =====
"use client"

import * as React from "react"
import * as TogglePrimitive from "@radix-ui/react-toggle"
import { cva } from "class-variance-authority";

import { cn } from "@/lib/utils"

const toggleVariants = cva(
  "inline-flex items-center justify-center gap-2 rounded-md text-sm font-medium transition-colors hover:bg-muted hover:text-muted-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 data-[state=on]:bg-accent data-[state=on]:text-accent-foreground [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-transparent",
        outline:
          "border border-input bg-transparent shadow-sm hover:bg-accent hover:text-accent-foreground",
      },
      size: {
        default: "h-9 px-2 min-w-9",
        sm: "h-8 px-1.5 min-w-8",
        lg: "h-10 px-2.5 min-w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

const Toggle = React.forwardRef(({ className, variant, size, ...props }, ref) => (
  <TogglePrimitive.Root
    ref={ref}
    className={cn(toggleVariants({ variant, size, className }))}
    {...props} />
))

Toggle.displayName = TogglePrimitive.Root.displayName

export { Toggle, toggleVariants }

===== FILE: frontend/src/components/ui/tooltip.jsx =====
import * as React from "react"
import * as TooltipPrimitive from "@radix-ui/react-tooltip"

import { cn } from "@/lib/utils"

const TooltipProvider = TooltipPrimitive.Provider

const Tooltip = TooltipPrimitive.Root

const TooltipTrigger = TooltipPrimitive.Trigger

const TooltipContent = React.forwardRef(({ className, sideOffset = 4, ...props }, ref) => (
  <TooltipPrimitive.Portal>
    <TooltipPrimitive.Content
      ref={ref}
      sideOffset={sideOffset}
      className={cn(
        "z-50 overflow-hidden rounded-md bg-primary px-3 py-1.5 text-xs text-primary-foreground animate-in fade-in-0 zoom-in-95 data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=closed]:zoom-out-95 data-[side=bottom]:slide-in-from-top-2 data-[side=left]:slide-in-from-right-2 data-[side=right]:slide-in-from-left-2 data-[side=top]:slide-in-from-bottom-2 origin-[--radix-tooltip-content-transform-origin]",
        className
      )}
      {...props} />
  </TooltipPrimitive.Portal>
))
TooltipContent.displayName = TooltipPrimitive.Content.displayName

export { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider }

===== FILE: frontend/src/constants/testIds/auth.js =====
// Test IDs for the auth feature (login, register, password reset, logout).
// Add new keys here as you wire up additional auth UI; see ./index.js for
// the recipe to add a new feature file.
//
// Directive:
//   - Keys are camelCase, values are kebab-case shaped as `<feature>-<element>`
//     (or `<feature>-<element>-<qualifier>` when an element repeats). Examples:
//     'login-submit-button', 'cart-quantity-input', 'product-card-image'.
//   - Reference them in JSX as `data-testid={LOGIN.submitButton}`.
//
// Why kebab-case values: required by qabot's CSS-attribute selector matcher
// and the lint rule `emergent(kebab-case-testid)`.

export const LOGIN = {
	emailInput: 'login-email-input',
	passwordInput: 'login-password-input',
	submitButton: 'login-submit-button',
	forgotPasswordLink: 'login-forgot-password-link',
	registerLink: 'login-register-link',
};

export const REGISTER = {
	nameInput: 'register-name-input',
	emailInput: 'register-email-input',
	passwordInput: 'register-password-input',
	passwordConfirmInput: 'register-password-confirm-input',
	submitButton: 'register-submit-button',
	loginLink: 'register-login-link',
};

export const LOGOUT = {
	button: 'logout-button',
};

===== FILE: frontend/src/constants/testIds/home.js =====
// Test IDs for the home / landing feature. Naming follows the directive
// in ./auth.js (keys camelCase, values kebab-case `<feature>-<element>`).

export const HOME = {
	emergentLink: 'home-emergent-link',
};

===== FILE: frontend/src/constants/testIds/index.js =====
// constants/testIds/ — central registry of data-testid values used by the
// end-to-end testing agent (qabot) to locate and interact with UI elements
// during automated tests. UI without testids cannot be automatically verified.
//
// Structure: each feature lives in its own file (auth.js, cart.js, ...) and
// is re-exported from here, so consumers can do a single import like
// `import { LOGIN, CART } from '@/constants/testIds'` (or relative).
//
// Adding a new feature:
//   1. Create constants/testIds/<feature>.js
//   2. Export named objects (e.g. `export const PROFILE = { ... }`)
//   3. Re-export here: `export * from './<feature>';`

export * from './auth';
export * from './home';

===== FILE: frontend/src/context/AuthContext.jsx =====
import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api } from "@/lib/api";

const AuthCtx = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadMe = useCallback(async () => {
    const token = localStorage.getItem("elo_token");
    if (!token) { setUser(null); setLoading(false); return; }
    try {
      const { data } = await api.get("/auth/me");
      setUser(data);
    } catch {
      localStorage.removeItem("elo_token");
      setUser(null);
    } finally { setLoading(false); }
  }, []);

  useEffect(() => {
    // Ao voltar do Google, o AuthCallback troca o session_id antes de qualquer /me.
    if (window.location.hash?.includes("session_id=")) { setLoading(false); return; }
    loadMe();
  }, [loadMe]);

  const login = async (email, senha) => {
    const { data } = await api.post("/auth/login", { email, senha });
    localStorage.setItem("elo_token", data.access_token);
    await loadMe();
  };

  const register = async (payload) => {
    const { data } = await api.post("/auth/register", payload);
    localStorage.setItem("elo_token", data.access_token);
    await loadMe();
  };

  const loginWithGoogle = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin + "/app/atendimento";
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  const processSession = async (sessionId) => {
    const { data } = await api.post("/auth/session", { session_id: sessionId });
    localStorage.setItem("elo_token", data.access_token);
    setUser(data.user);
    setLoading(false);
    return data.user;
  };

  const logout = async () => {
    try { await api.post("/auth/logout"); } catch { /* sessão já inválida */ }
    localStorage.removeItem("elo_token");
    setUser(null);
  };

  const updateProfile = async (payload) => {
    const { data } = await api.put("/auth/me", payload);
    setUser(data);
    return data;
  };

  return (
    <AuthCtx.Provider value={{ user, loading, login, register, loginWithGoogle, processSession, logout, updateProfile }}>
      {children}
    </AuthCtx.Provider>
  );
}

export const useAuth = () => useContext(AuthCtx);

===== FILE: frontend/src/context/ToastContext.jsx =====
import { createContext, useCallback, useContext, useState } from "react";

const Ctx = createContext(null);

export function ToastProvider({ children }) {
  const [items, setItems] = useState([]);
  const push = useCallback((message, variant = "default") => {
    const id = Math.random().toString(36).slice(2);
    setItems((v) => [...v, { id, message, variant }]);
    setTimeout(() => setItems((v) => v.filter((t) => t.id !== id)), 3000);
  }, []);
  return (
    <Ctx.Provider value={push}>
      {children}
      <div className="toasts" data-testid="toast-root">
        {items.map((t) => (
          <div key={t.id} className={`toast ${t.variant}`} data-testid={`toast-${t.variant}`}>{t.message}</div>
        ))}
      </div>
    </Ctx.Provider>
  );
}

export const useToast = () => useContext(Ctx);

===== FILE: frontend/src/hooks/use-toast.js =====
"use client";
// Inspired by react-hot-toast library
import * as React from "react"

const TOAST_LIMIT = 1
const TOAST_REMOVE_DELAY = 1000000

const actionTypes = {
  ADD_TOAST: "ADD_TOAST",
  UPDATE_TOAST: "UPDATE_TOAST",
  DISMISS_TOAST: "DISMISS_TOAST",
  REMOVE_TOAST: "REMOVE_TOAST"
}

let count = 0

function genId() {
  count = (count + 1) % Number.MAX_SAFE_INTEGER
  return count.toString();
}

const toastTimeouts = new Map()

const addToRemoveQueue = (toastId) => {
  if (toastTimeouts.has(toastId)) {
    return
  }

  const timeout = setTimeout(() => {
    toastTimeouts.delete(toastId)
    dispatch({
      type: "REMOVE_TOAST",
      toastId: toastId,
    })
  }, TOAST_REMOVE_DELAY)

  toastTimeouts.set(toastId, timeout)
}

export const reducer = (state, action) => {
  switch (action.type) {
    case "ADD_TOAST":
      return {
        ...state,
        toasts: [action.toast, ...state.toasts].slice(0, TOAST_LIMIT),
      };

    case "UPDATE_TOAST":
      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === action.toast.id ? { ...t, ...action.toast } : t),
      };

    case "DISMISS_TOAST": {
      const { toastId } = action

      // ! Side effects ! - This could be extracted into a dismissToast() action,
      // but I'll keep it here for simplicity
      if (toastId) {
        addToRemoveQueue(toastId)
      } else {
        state.toasts.forEach((toast) => {
          addToRemoveQueue(toast.id)
        })
      }

      return {
        ...state,
        toasts: state.toasts.map((t) =>
          t.id === toastId || toastId === undefined
            ? {
                ...t,
                open: false,
              }
            : t),
      };
    }
    case "REMOVE_TOAST":
      if (action.toastId === undefined) {
        return {
          ...state,
          toasts: [],
        }
      }
      return {
        ...state,
        toasts: state.toasts.filter((t) => t.id !== action.toastId),
      };
  }
}

const listeners = []

let memoryState = { toasts: [] }

function dispatch(action) {
  memoryState = reducer(memoryState, action)
  listeners.forEach((listener) => {
    listener(memoryState)
  })
}

function toast({
  ...props
}) {
  const id = genId()

  const update = (props) =>
    dispatch({
      type: "UPDATE_TOAST",
      toast: { ...props, id },
    })
  const dismiss = () => dispatch({ type: "DISMISS_TOAST", toastId: id })

  dispatch({
    type: "ADD_TOAST",
    toast: {
      ...props,
      id,
      open: true,
      onOpenChange: (open) => {
        if (!open) dismiss()
      },
    },
  })

  return {
    id: id,
    dismiss,
    update,
  }
}

function useToast() {
  const [state, setState] = React.useState(memoryState)

  React.useEffect(() => {
    listeners.push(setState)
    return () => {
      const index = listeners.indexOf(setState)
      if (index > -1) {
        listeners.splice(index, 1)
      }
    };
  }, [state])

  return {
    ...state,
    toast,
    dismiss: (toastId) => dispatch({ type: "DISMISS_TOAST", toastId }),
  };
}

export { useToast, toast }

===== FILE: frontend/src/index.css =====
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,500;1,600;1,700&display=swap');

:root {
  --wine: #5c2c3b;
  --wine-2: #803a50;
  --wine-3: #4a2230;
  --rose: #e8c4d0;
  --rose-soft: #f8eef2;
  --ink: #3a1c26;
  --muted: #846875;
  --line: #eadde2;
  --paper: #fffafc;
  --green: #588b6a;
  --green-soft: #e5f1e7;
  --gold: #b58a47;
  --gold-soft: #f6eedf;
  --red: #bb5665;
  --red-soft: #fae5e8;
  --shadow: 0 10px 28px rgba(92, 44, 59, .10);
  --shadow-lg: 0 24px 60px rgba(58, 28, 38, .22);
}

* { box-sizing: border-box; }
html, body, #root { margin: 0; padding: 0; height: 100%; }
body {
  background: var(--paper);
  color: var(--ink);
  font-family: 'DM Sans', system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
h1, h2, h3, h4 { font-family: 'Playfair Display', serif; margin: 0; font-weight: 600; letter-spacing: -0.01em; }
p { margin: 0; }
button { font: inherit; color: inherit; cursor: pointer; }
input, select, textarea { font: inherit; color: inherit; outline: none; }
::selection { background: var(--rose); color: var(--ink); }

/* ---------------- LANDING / AUTH ---------------- */
.landing {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  background: var(--paper);
}
@media (max-width: 900px) { .landing { grid-template-columns: 1fr; } }

.landing-hero {
  position: relative;
  overflow: hidden;
  background: linear-gradient(180deg, rgba(92,44,59,.55), rgba(58,28,38,.75)),
              url('https://images.unsplash.com/photo-1560066984-138dadb4c035?w=1400&q=80') center/cover no-repeat;
  color: #fff;
  padding: 64px 72px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
@media (max-width: 900px) { .landing-hero { min-height: 300px; padding: 40px; } }

.landing-eyebrow {
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--rose);
  font-weight: 700;
}
.landing-hero h1 {
  font-family: 'Playfair Display', serif;
  font-weight: 600;
  font-size: 88px;
  line-height: 1.02;
  margin: 24px 0 22px;
  letter-spacing: -0.02em;
}
.landing-hero h1 em { color: var(--rose); font-style: italic; }
.landing-hero p {
  font-size: 16px;
  max-width: 460px;
  line-height: 1.6;
  color: #f2dee5;
}
@media (max-width: 1100px) { .landing-hero h1 { font-size: 64px; } }
@media (max-width: 900px) { .landing-hero h1 { font-size: 44px; } }

.landing-panel {
  padding: 64px 72px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  max-width: 640px;
}
@media (max-width: 900px) { .landing-panel { padding: 48px 32px; } }

.brand { display: flex; align-items: baseline; gap: 12px; color: var(--wine); margin-bottom: 96px; }
.brand-mark { font-family: 'Playfair Display', serif; font-size: 34px; font-weight: 700; letter-spacing: 6px; color: var(--wine); }
.brand-tagline { font-size: 15px; letter-spacing: 3px; color: var(--muted); text-transform: lowercase; font-weight: 500; }

.panel-eyebrow {
  font-size: 11px;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 700;
  margin-bottom: 20px;
}
.landing-panel h2 {
  font-family: 'Playfair Display', serif;
  font-size: 46px;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 14px;
  letter-spacing: -0.01em;
}
.landing-panel .lead {
  color: var(--muted);
  font-size: 15px;
  line-height: 1.6;
  margin-bottom: 32px;
}

.search-input {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 18px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: #fff;
  margin-bottom: 12px;
  transition: border .2s;
}
.search-input:focus-within { border-color: var(--wine-2); }
.search-input svg { color: var(--muted); flex: none; }
.search-input input { flex: 1; border: 0; background: transparent; font-size: 15px; color: var(--ink); }
.search-input input::placeholder { color: var(--muted); }

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 16px 22px;
  border: 1px solid transparent;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 600;
  transition: transform .12s, background .2s, border-color .2s, color .2s;
  width: 100%;
  text-decoration: none;
}
.btn:active { transform: scale(.98); }
.btn-primary { background: var(--wine-2); color: #fff; }
.btn-primary:hover { background: var(--wine); }
.btn-outline { background: transparent; color: var(--wine); border-color: var(--line); }
.btn-outline:hover { border-color: var(--wine-2); color: var(--wine); }
.btn-danger { background: var(--red); color: #fff; }
.btn-ghost { background: transparent; border: 0; color: var(--wine); padding: 10px 14px; font-weight: 600; font-size: 13px; }

.btn-stack { display: grid; gap: 10px; margin-top: 6px; }

.landing-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 24px;
  font-size: 12px;
  color: var(--muted);
}
.landing-footer strong { color: var(--wine); font-weight: 600; }

/* ---------------- MODAL ---------------- */
.modal-backdrop {
  position: fixed; inset: 0;
  background: rgba(58, 28, 38, 0.55);
  backdrop-filter: blur(4px);
  z-index: 100;
  display: grid;
  place-items: center;
  padding: 20px;
  animation: fadeIn .16s ease;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
.modal-card {
  background: #fff;
  width: 100%;
  max-width: 440px;
  border-radius: 6px;
  padding: 40px 40px 36px;
  box-shadow: 0 30px 80px rgba(0,0,0,.3);
  animation: modalUp .22s ease;
}
@keyframes modalUp { from { transform: translateY(20px); opacity: 0; } to { transform: none; opacity: 1; } }
.modal-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 22px; }
.modal-eyebrow { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--muted); font-weight: 700; }
.modal-close { border: 0; background: transparent; color: var(--muted); padding: 4px; border-radius: 4px; }
.modal-close:hover { color: var(--ink); }
.modal-card h3 { font-family: 'Playfair Display', serif; font-size: 30px; margin-top: 8px; margin-bottom: 8px; }
.modal-card p.hint { color: var(--muted); font-size: 14px; line-height: 1.55; margin-bottom: 24px; }
.modal-card .field { display: block; margin-bottom: 12px; }
.modal-card .field input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: 4px;
  font-size: 14px;
  background: #fff;
  color: var(--ink);
  transition: border .2s;
}
.modal-card .field input:focus { border-color: var(--wine-2); }
.modal-card .btn { margin-top: 10px; }
.modal-error { color: var(--red); font-size: 12.5px; margin-top: 8px; }

/* Auth extras */
.btn-google { background: #fff; color: var(--ink); border-color: var(--line); }
.btn-google:hover { border-color: var(--wine-2); background: var(--paper); }
.btn-google svg { flex: none; }
.auth-divider { display: flex; align-items: center; gap: 12px; color: var(--muted); font-size: 11px; letter-spacing: 2px; text-transform: uppercase; margin: 18px 0 6px; }
.auth-divider::before, .auth-divider::after { content: ''; flex: 1; height: 1px; background: var(--line); }
.auth-switch { font-size: 13px; color: var(--muted); margin-top: 18px; text-align: center; }
.auth-switch button { background: none; border: 0; padding: 0; color: var(--wine-2); font-weight: 600; text-decoration: underline; text-underline-offset: 3px; }
.auth-switch button:hover { color: var(--wine); }

/* ---------------- APP SHELL (dashboard) ---------------- */
.app-shell { display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; background: #faf6f7; }
.sidebar {
  background: var(--wine);
  color: #f2dee5;
  padding: 32px 22px 24px;
  display: flex;
  flex-direction: column;
  gap: 30px;
  position: sticky;
  top: 0;
  height: 100vh;
}
.sidebar-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 4px 20px;
  border-bottom: 1px solid rgba(255,255,255,.08);
}
.sidebar-brand .mono {
  width: 42px; height: 42px; border-radius: 50%;
  border: 1.5px solid rgba(255,255,255,.35);
  display: grid; place-items: center;
  font-family: 'Playfair Display', serif; font-size: 20px; font-weight: 600;
  color: #fff;
}
.sidebar-brand strong { font-family: 'Playfair Display', serif; font-size: 21px; font-weight: 700; letter-spacing: 3px; color: #fff; display: block; }
.sidebar-brand small { display: block; font-size: 10px; letter-spacing: 2.5px; color: var(--rose); margin-top: 2px; }

.sidebar-eyebrow { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: rgba(255,255,255,.5); font-weight: 700; margin-left: 4px; }
.sidebar-nav { display: flex; flex-direction: column; gap: 4px; margin-top: 10px; }
.sidebar-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 14px;
  border-radius: 6px;
  background: transparent;
  color: #f2dee5;
  border: 0;
  font-size: 14px; font-weight: 500;
  text-align: left; width: 100%;
  transition: background .18s, color .18s;
  text-decoration: none;
}
.sidebar-item:hover { background: rgba(255,255,255,.06); color: #fff; }
.sidebar-item.active { background: rgba(255,255,255,.12); color: #fff; font-weight: 600; }
.sidebar-item svg { flex: none; opacity: .85; }
.sidebar-item.active svg { opacity: 1; }
.sidebar-bottom { margin-top: auto; padding-top: 20px; border-top: 1px solid rgba(255,255,255,.08); }

.main { display: flex; flex-direction: column; min-width: 0; }
.topbar {
  display: flex; align-items: center; gap: 16px;
  padding: 20px 40px;
  border-bottom: 1px solid var(--line);
  background: #fff;
}
.topbar-crumbs { display: flex; align-items: center; gap: 10px; color: var(--muted); font-size: 13px; font-weight: 500; flex: 1; }
.topbar-crumbs .active { color: var(--wine); font-weight: 700; }
.topbar-crumbs .sep { color: var(--rose); }
.topbar-search {
  flex: 1; max-width: 460px;
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--paper);
}
.topbar-search input { flex: 1; border: 0; background: transparent; font-size: 13.5px; }
.topbar-kbd { background: #fff; border: 1px solid var(--line); border-radius: 4px; padding: 2px 6px; font-size: 10.5px; color: var(--muted); font-family: monospace; }
.topbar-icon { border: 0; background: transparent; color: var(--wine); width: 38px; height: 38px; border-radius: 50%; display: grid; place-items: center; }
.topbar-icon:hover { background: var(--rose-soft); }
.topbar-user { display: flex; align-items: center; gap: 10px; }
.topbar-avatar { width: 36px; height: 36px; border-radius: 50%; background: var(--wine); color: #fff; display: grid; place-items: center; font-family: 'Playfair Display', serif; font-weight: 600; font-size: 13px; }
.topbar-user strong { font-size: 13px; }
.topbar-user small { display: block; font-size: 11px; color: var(--muted); }

.content { padding: 40px; flex: 1; max-width: 1600px; width: 100%; }
.content-eyebrow { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: var(--muted); font-weight: 700; margin-bottom: 14px; }
.content h1.page-title { font-family: 'Playfair Display', serif; font-size: 56px; font-weight: 600; letter-spacing: -0.02em; line-height: 1.05; margin-bottom: 10px; }
.content .page-sub { color: var(--muted); font-size: 15px; line-height: 1.55; max-width: 620px; margin-bottom: 32px; }

.cta-inline { display: flex; justify-content: space-between; align-items: flex-start; gap: 24px; flex-wrap: wrap; margin-bottom: 32px; }
.cta-inline .actions { display: flex; gap: 10px; }
.btn-inline { display: inline-flex; align-items: center; gap: 8px; padding: 14px 22px; border-radius: 4px; font-weight: 600; font-size: 14px; border: 1px solid transparent; }
.btn-wa { background: #1eaf5b; color: #fff; }
.btn-wa:hover { background: #17994e; }

/* ---------------- CARDS ---------------- */
.card {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 26px;
  box-shadow: 0 1px 2px rgba(58,28,38,.03);
}
.card-eyebrow { font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--muted); font-weight: 700; margin-bottom: 8px; }
.card h3 { font-family: 'Playfair Display', serif; font-size: 24px; font-weight: 600; margin-bottom: 6px; }
.card p.desc { color: var(--muted); font-size: 13.5px; line-height: 1.55; margin-bottom: 20px; }

.grid-3 { display: grid; grid-template-columns: 1.2fr 1fr 1.2fr; gap: 20px; align-items: start; }
@media (max-width: 1100px) { .grid-3 { grid-template-columns: 1fr; } }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
@media (max-width: 900px) { .grid-2 { grid-template-columns: 1fr; } }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
@media (max-width: 1100px) { .grid-4 { grid-template-columns: repeat(2, 1fr); } }

.field { display: block; font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 16px; letter-spacing: 0.02em; }
.field input, .field select, .field textarea {
  display: block;
  width: 100%;
  margin-top: 6px;
  padding: 12px 14px;
  border: 1px solid var(--line);
  border-radius: 4px;
  background: #fff;
  font-size: 14px;
  color: var(--ink);
  font-weight: 400;
  transition: border .2s;
}
.field input:focus, .field select:focus, .field textarea:focus { border-color: var(--wine-2); }
.field textarea { resize: vertical; min-height: 90px; }

.list-item { display: flex; align-items: center; gap: 14px; padding: 16px 4px; border-bottom: 1px solid var(--line); position: relative; }
.list-item:last-child { border-bottom: 0; }
.list-item.active { padding-left: 18px; }
.list-item.active::before { content: ''; position: absolute; left: 0; top: 12px; bottom: 12px; width: 3px; background: var(--wine-2); border-radius: 2px; }
.avatar-sm { width: 40px; height: 40px; border-radius: 50%; background: var(--rose); color: var(--wine); display: grid; place-items: center; font-weight: 600; font-size: 13px; flex: none; }
.avatar-sm.green { background: var(--green-soft); color: var(--green); }
.list-item div.body { flex: 1; min-width: 0; }
.list-item strong { display: block; font-size: 14px; font-weight: 600; }
.list-item span.sub { display: block; font-size: 12.5px; color: var(--muted); margin-top: 2px; }
.list-item small.meta { font-size: 11.5px; color: var(--muted); flex: none; }

.badge { display: inline-flex; padding: 3px 10px; font-size: 10.5px; font-weight: 700; border-radius: 12px; letter-spacing: 0.02em; }
.badge.rose { background: var(--rose-soft); color: var(--wine); }
.badge.green { background: var(--green-soft); color: var(--green); }
.badge.gold { background: var(--gold-soft); color: var(--gold); }
.badge.red { background: var(--red-soft); color: var(--red); }

/* Chat */
.chat-card { display: flex; flex-direction: column; min-height: 520px; }
.chat-header { display: flex; align-items: center; gap: 12px; padding-bottom: 18px; border-bottom: 1px solid var(--line); margin-bottom: 20px; }
.chat-header .body { flex: 1; }
.chat-header strong { display: block; font-size: 14px; }
.chat-header small { display: block; font-size: 12px; color: var(--muted); }
.chat-status { width: 8px; height: 8px; border-radius: 50%; background: var(--green); }
.messages { flex: 1; display: flex; flex-direction: column; gap: 10px; padding-bottom: 16px; max-height: 420px; overflow-y: auto; scrollbar-width: thin; }
.msg { max-width: 78%; padding: 12px 14px; border-radius: 12px; font-size: 13px; line-height: 1.5; white-space: pre-wrap; word-break: break-word; }
.msg.bot { background: var(--rose-soft); color: var(--ink); align-self: flex-start; border-bottom-left-radius: 4px; }
.msg.user { background: var(--wine); color: #fff; align-self: flex-end; border-bottom-right-radius: 4px; }
.msg.typing::after { content: '▍'; margin-left: 2px; color: var(--wine-2); animation: blink 1s steps(2) infinite; }
@keyframes blink { 50% { opacity: 0; } }
.chat-input { display: flex; gap: 8px; align-items: center; border-top: 1px solid var(--line); padding-top: 16px; }
.chat-input input { flex: 1; padding: 11px 14px; border: 1px solid var(--line); border-radius: 24px; font-size: 13px; }
.chat-input input:focus { border-color: var(--wine-2); }
.chat-input button { border: 0; background: var(--wine); color: #fff; width: 42px; height: 42px; border-radius: 50%; display: grid; place-items: center; transition: background .2s, opacity .2s; }
.chat-input button:disabled { opacity: .45; cursor: not-allowed; }

/* AI helpers */
.field-row { display: flex; justify-content: space-between; align-items: center; gap: 10px; }
.btn-ai { display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 999px; border: 1px solid var(--gold); background: var(--gold-soft); color: var(--gold); font-size: 11.5px; font-weight: 700; letter-spacing: .02em; transition: background .2s, color .2s, transform .12s; }
.btn-ai:hover { background: var(--gold); color: #fff; }
.btn-ai:active { transform: scale(.97); }
.btn-ai:disabled { opacity: .6; cursor: progress; }
.btn-ai.lg { padding: 11px 18px; font-size: 13px; }
.btn-inline.primary { background: var(--wine-2); color: #fff; }
.btn-inline.primary:hover { background: var(--wine); }
.btn-inline:disabled { opacity: .45; cursor: not-allowed; }
.btn-inline.small { padding: 8px 14px; font-size: 12.5px; }
.btn-inline.disabled { opacity: .45; pointer-events: none; }

/* Lembretes de véspera */
.vespera-card { border-top: 4px solid var(--gold); }
.vespera-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 20px; flex-wrap: wrap; }
.vespera-head .desc { margin-bottom: 8px; }
.vespera-cta { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.vespera-note { display: flex; align-items: flex-start; gap: 10px; background: var(--gold-soft); color: #7a5a24; border-radius: 6px; padding: 12px 14px; font-size: 12.5px; line-height: 1.5; margin: 14px 0 6px; }
.vespera-note svg { flex: none; margin-top: 2px; color: var(--gold); }
.vespera-note code { background: rgba(255,255,255,.7); padding: 1px 6px; border-radius: 4px; font-size: 11.5px; }
.vespera-list { display: grid; gap: 12px; margin-top: 18px; }
.vespera-row { display: grid; grid-template-columns: minmax(240px, 1.1fr) 2fr auto; gap: 16px; align-items: center; padding: 16px 18px; border: 1px solid var(--line); border-left: 4px solid var(--wine-2); border-radius: 6px; background: #fff; transition: border-color .2s, background .2s; }
.vespera-row.sent { border-left-color: var(--green); background: #fbfdfb; }
@media (max-width: 1100px) { .vespera-row { grid-template-columns: 1fr; } }
.vespera-who { display: flex; align-items: center; gap: 12px; min-width: 0; }
.vespera-who .body { flex: 1; min-width: 0; }
.vespera-who strong { display: block; font-size: 14px; }
.vespera-who .sub { display: block; font-size: 12px; color: var(--muted); margin-top: 2px; }
.vespera-who .mono-tel { font-family: ui-monospace, monospace; font-size: 11.5px; }
.vespera-who .badge { display: inline-flex; align-items: center; gap: 4px; white-space: nowrap; }
.vespera-text { width: 100%; padding: 10px 12px; border: 1px solid var(--line); border-radius: 6px; font-size: 13px; line-height: 1.5; resize: vertical; min-height: 56px; background: var(--paper); transition: border .2s; }
.vespera-text:focus { border-color: var(--wine-2); background: #fff; }
.vespera-actions { display: flex; gap: 8px; align-items: center; }

/* Insumos por serviço */
.servico-block { border-bottom: 1px solid var(--line); }
.servico-block:last-of-type { border-bottom: 0; }
.servico-block .list-item { border-bottom: 0; }
.si-wrap { padding: 0 4px 12px 54px; }
.si-toggle { display: inline-flex; align-items: center; gap: 6px; background: none; border: 0; padding: 4px 0; font-size: 12px; font-weight: 600; color: var(--wine-2); letter-spacing: .02em; }
.si-toggle:hover { color: var(--wine); }
.si-panel { margin-top: 10px; padding: 12px 14px; background: var(--rose-soft); border-radius: 6px; display: grid; gap: 8px; animation: fadeIn .16s ease; }
.si-empty { font-size: 12.5px; color: var(--muted); line-height: 1.5; }
.si-row { display: flex; align-items: center; gap: 10px; font-size: 13px; }
.si-name { flex: 1; font-weight: 600; }
.si-qty { font-size: 12px; color: var(--muted); white-space: nowrap; }
.si-form { display: grid; grid-template-columns: 1fr 90px auto; gap: 8px; margin-top: 4px; }
.si-form select, .si-form input { padding: 9px 10px; border: 1px solid var(--line); border-radius: 4px; background: #fff; font-size: 13px; }
.si-form select:focus, .si-form input:focus { border-color: var(--wine-2); }

/* Agenda / Calendar */
.day-strip { display: flex; gap: 10px; overflow-x: auto; padding: 4px 2px 20px; }
.day-chip { flex: none; width: 74px; padding: 14px 0; border-radius: 8px; border: 1px solid var(--line); background: #fff; text-align: center; cursor: pointer; transition: all .15s; }
.day-chip.selected { background: var(--wine); border-color: var(--wine); color: #fff; }
.day-chip.today { border-color: var(--wine-2); }
.day-chip .dow { display: block; font-size: 10.5px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--muted); font-weight: 700; margin-bottom: 6px; }
.day-chip.selected .dow { color: var(--rose); }
.day-chip .num { display: block; font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 600; }

.booking-item { display: flex; gap: 16px; align-items: center; padding: 16px 20px; border: 1px solid var(--line); border-left: 4px solid var(--wine-2); border-radius: 6px; margin-bottom: 10px; background: #fff; }
.booking-item.green { border-left-color: var(--green); }
.booking-item.gold { border-left-color: var(--gold); }
.booking-time { min-width: 62px; }
.booking-time strong { display: block; font-family: 'Playfair Display', serif; font-size: 18px; }
.booking-time small { display: block; font-size: 11px; color: var(--muted); margin-top: 2px; }
.booking-body { flex: 1; }
.booking-body strong { display: block; font-size: 14px; }
.booking-body small { display: block; font-size: 12px; color: var(--muted); margin-top: 3px; }

/* Finance */
.finance-hero { background: linear-gradient(135deg, var(--wine), var(--wine-3)); color: #fff; padding: 32px; border-radius: 8px; }
.finance-hero .lbl { font-size: 11px; letter-spacing: 2.5px; text-transform: uppercase; color: var(--rose); font-weight: 700; }
.finance-hero .val { display: block; font-family: 'Playfair Display', serif; font-size: 56px; font-weight: 600; margin: 12px 0 8px; }
.finance-hero .sub { font-size: 13px; color: var(--rose); }

.fin-summary { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 22px; }
.fin-summary div { background: var(--rose-soft); border-radius: 6px; padding: 16px; }
.fin-summary .k { font-size: 10.5px; letter-spacing: 2px; text-transform: uppercase; color: var(--muted); font-weight: 700; }
.fin-summary .v { display: block; margin-top: 6px; font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 600; color: var(--wine); }

/* Toast */
.toasts { position: fixed; bottom: 24px; right: 24px; z-index: 200; display: flex; flex-direction: column; gap: 8px; }
.toast { background: var(--ink); color: #fff; padding: 12px 18px; border-radius: 24px; font-size: 13px; font-weight: 500; box-shadow: 0 12px 32px rgba(0,0,0,.3); animation: toastIn .18s ease; }
.toast.success { background: var(--green); }
.toast.error { background: var(--red); }
.toast.warning { background: var(--gold); }
@keyframes toastIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }

.empty { padding: 44px 22px; text-align: center; color: var(--muted); }
.empty h4 { font-family: 'Playfair Display', serif; font-size: 20px; color: var(--ink); margin-bottom: 6px; }
.empty p { font-size: 13.5px; line-height: 1.55; }

.loading { padding: 40px; text-align: center; color: var(--muted); font-size: 13px; }

===== FILE: frontend/src/index.js =====
import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "@/index.css";
import App from "@/App";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,
      refetchOnWindowFocus: false,
    },
  },
});

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
);

===== FILE: frontend/src/lib/api.js =====
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API_BASE = `${BACKEND_URL}/api`;

export const api = axios.create({ baseURL: API_BASE, withCredentials: true });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("elo_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export async function streamSSE(path, body, { onDelta, onMeta, signal } = {}) {
  const token = localStorage.getItem("elo_token");
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    credentials: "include",
    signal,
    headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}) },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Falha ao falar com a IA");
  }
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    const events = buffer.split("\n\n");
    buffer = events.pop();
    for (const raw of events) {
      const line = raw.split("\n").find((l) => l.startsWith("data: "));
      if (!line) continue;
      const ev = JSON.parse(line.slice(6));
      if (ev.error) throw new Error(ev.error);
      if (ev.delta) onDelta?.(ev.delta);
      else onMeta?.(ev);
    }
  }
}

===== FILE: frontend/src/lib/utils.js =====
import { clsx } from "clsx";
import { twMerge } from "tailwind-merge"

export function cn(...inputs) {
  return twMerge(clsx(inputs));
}

===== FILE: frontend/src/pages/Agenda.jsx =====
import { useEffect, useMemo, useState } from "react";
import { Plus, Check, Trash2 } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

function fmtDay(d) {
  return { dow: d.toLocaleDateString("pt-BR", { weekday: "short" }).slice(0, 3).toUpperCase(), num: d.getDate() };
}

export default function Agenda() {
  const toast = useToast();
  const today = useMemo(() => new Date(new Date().setHours(0,0,0,0)), []);
  const [selected, setSelected] = useState(today);
  const [agendamentos, setAgendamentos] = useState([]);
  const [servicos, setServicos] = useState([]);
  const [profs, setProfs] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ cliente_nome: "", cliente_telefone: "", servico_id: "", profissional_id: "", hora: "10:00" });

  const days = useMemo(() => {
    const arr = [];
    for (let i = -1; i < 6; i++) {
      const d = new Date(today); d.setDate(today.getDate() + i); arr.push(d);
    }
    return arr;
  }, [today]);

  const loadAll = async () => {
    const start = new Date(selected); start.setHours(0,0,0,0);
    const end = new Date(start); end.setDate(end.getDate() + 1);
    try {
      const [{ data: ags }, { data: srv }, { data: pro }] = await Promise.all([
        api.get("/agendamentos/", { params: { data_inicio: start.toISOString(), data_fim: end.toISOString() } }),
        api.get("/servicos/"),
        api.get("/profissionais/"),
      ]);
      setAgendamentos(ags);
      setServicos(srv);
      setProfs(pro);
    } catch { toast("Erro ao carregar agenda", "error"); }
  };

  useEffect(() => { loadAll(); /* eslint-disable-next-line */ }, [selected]);

  const criar = async (e) => {
    e.preventDefault();
    if (!form.servico_id || !form.profissional_id || !form.cliente_telefone) { toast("Preencha todos os campos", "error"); return; }
    const inicio = new Date(selected);
    const [h, m] = form.hora.split(":").map(Number);
    inicio.setHours(h, m, 0, 0);
    try {
      await api.post("/agendamentos/", {
        servico_id: form.servico_id,
        profissional_id: form.profissional_id,
        cliente_telefone: form.cliente_telefone,
        cliente_nome: form.cliente_nome || null,
        data_hora_inicio: inicio.toISOString(),
      });
      toast("Agendamento criado", "success");
      setShowForm(false);
      setForm({ cliente_nome: "", cliente_telefone: "", servico_id: "", profissional_id: "", hora: "10:00" });
      loadAll();
    } catch (ex) {
      toast(ex.response?.data?.detail || "Erro ao criar", "error");
    }
  };

  const concluir = async (id) => {
    try {
      const { data } = await api.patch(`/agendamentos/${id}/concluir`);
      toast("Atendimento concluído — estoque atualizado", "success");
      (data.alertas_estoque || []).forEach((a) => toast(a, "warning"));
      loadAll();
    } catch (ex) { toast(ex.response?.data?.detail || "Erro", "error"); }
  };
  const remover = async (id) => {
    try { await api.delete(`/agendamentos/${id}`); toast("Excluído", "success"); loadAll(); }
    catch { toast("Erro", "error"); }
  };

  return (
    <div data-testid="agenda-page">
      <div className="cta-inline">
        <div>
          <span className="content-eyebrow">Espaço de gestão</span>
          <h1 className="page-title">Agenda</h1>
          <p className="page-sub">Acompanhe os atendimentos do dia com uma visão calma e organizada.</p>
        </div>
        <div className="actions">
          <button className="btn-inline" style={{ background: "var(--wine-2)", color: "#fff" }} onClick={() => setShowForm(true)} data-testid="btn-new-agendamento">
            <Plus size={16} /> Novo agendamento
          </button>
        </div>
      </div>

      <div className="day-strip" data-testid="day-strip">
        {days.map((d) => {
          const isSel = d.toDateString() === selected.toDateString();
          const isToday = d.toDateString() === today.toDateString();
          const { dow, num } = fmtDay(d);
          return (
            <button key={d.toISOString()} className={`day-chip ${isSel ? "selected" : ""} ${isToday ? "today" : ""}`} onClick={() => setSelected(d)} data-testid={`day-${num}`}>
              <span className="dow">{dow}</span>
              <span className="num">{num}</span>
            </button>
          );
        })}
      </div>

      <div className="grid-2">
        <section className="card" data-testid="card-hoje">
          <span className="card-eyebrow">{selected.toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long" })}</span>
          <h3>Agendamentos do dia</h3>
          <p className="desc">{agendamentos.length} atendimento(s) programado(s).</p>

          {agendamentos.length === 0 && (
            <div className="empty" data-testid="empty-agenda">
              <h4>Sem agendamentos</h4>
              <p>Nenhum compromisso registrado para esta data.</p>
            </div>
          )}
          {agendamentos.map((a, i) => {
            const inicio = new Date(a.data_hora_inicio);
            const color = a.status === "concluido" ? "green" : (i % 3 === 2 ? "gold" : "");
            return (
              <div key={a.id} className={`booking-item ${color}`} data-testid={`booking-${a.id}`}>
                <div className="booking-time">
                  <strong>{inicio.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}</strong>
                  <small>{a.servico_nome}</small>
                </div>
                <div className="booking-body">
                  <strong>{a.cliente_nome || "Cliente"}</strong>
                  <small>com {a.profissional_nome} • R$ {a.servico_valor.toFixed(2)}</small>
                </div>
                <span className={`badge ${a.status === "concluido" ? "green" : "rose"}`}>{a.status}</span>
                {a.status !== "concluido" && (
                  <button className="topbar-icon" onClick={() => concluir(a.id)} data-testid={`btn-concluir-${a.id}`} title="Concluir">
                    <Check size={16} />
                  </button>
                )}
                <button className="topbar-icon" onClick={() => remover(a.id)} data-testid={`btn-del-${a.id}`} title="Excluir">
                  <Trash2 size={16} />
                </button>
              </div>
            );
          })}
        </section>

        {showForm && (
          <section className="card" data-testid="card-form-agendamento">
            <span className="card-eyebrow">Novo compromisso</span>
            <h3>Registrar agendamento</h3>
            <p className="desc">Selecione o cliente, serviço e horário desejado.</p>
            <form onSubmit={criar}>
              <label className="field">Nome do cliente
                <input value={form.cliente_nome} onChange={(e) => setForm({ ...form, cliente_nome: e.target.value })} data-testid="form-cliente-nome" />
              </label>
              <label className="field">Telefone (DDI+DDD)
                <input value={form.cliente_telefone} onChange={(e) => setForm({ ...form, cliente_telefone: e.target.value })} placeholder="5511990000000" data-testid="form-cliente-tel" required />
              </label>
              <div className="grid-2">
                <label className="field">Serviço
                  <select value={form.servico_id} onChange={(e) => setForm({ ...form, servico_id: e.target.value })} data-testid="form-servico" required>
                    <option value="">Selecione</option>
                    {servicos.map((s) => <option key={s.id} value={s.id}>{s.nome} — R${s.valor.toFixed(2)}</option>)}
                  </select>
                </label>
                <label className="field">Profissional
                  <select value={form.profissional_id} onChange={(e) => setForm({ ...form, profissional_id: e.target.value })} data-testid="form-prof" required>
                    <option value="">Selecione</option>
                    {profs.map((p) => <option key={p.id} value={p.id}>{p.nome}</option>)}
                  </select>
                </label>
              </div>
              <label className="field">Horário
                <input type="time" value={form.hora} onChange={(e) => setForm({ ...form, hora: e.target.value })} data-testid="form-hora" required />
              </label>
              <div className="grid-2">
                <button type="submit" className="btn btn-primary" data-testid="form-submit">Confirmar</button>
                <button type="button" className="btn btn-outline" onClick={() => setShowForm(false)}>Cancelar</button>
              </div>
            </form>
          </section>
        )}
      </div>
    </div>
  );
}

===== FILE: frontend/src/pages/Atendimento.jsx =====
import { useEffect, useRef, useState } from "react";
import { Phone, Send, MessageCircle, Sparkles, RotateCcw, ArrowUp } from "lucide-react";
import { api, streamSSE } from "@/lib/api";
import { useToast } from "@/context/ToastContext";
import LembretesVespera from "@/components/LembretesVespera";

const SESSION_KEY = "elo_chat_session";
const WELCOME = { role: "assistant", content: "Olá! Sou o Assistente ELO. Posso ajudar com a agenda de hoje, mensagens para clientes, estoque ou finanças. O que você precisa?" };

const DEMO_CONVERSAS = [
  { id: "c1", nome: "Amanda Martins", initials: "AM", ultima: "Posso agendar para sexta?", hora: "10:42", ativa: true },
  { id: "c2", nome: "João Costa", initials: "JC", ultima: "Obrigado pelo atendimento!", hora: "Ontem", green: true },
];

export default function Atendimento() {
  const toast = useToast();
  const [numero, setNumero] = useState("");
  const [clienteNome, setClienteNome] = useState("");
  const [mensagem, setMensagem] = useState("Olá! Passando para lembrar do seu atendimento na ELO Beauty Care. Confirma pra mim? 💕");
  const [gerando, setGerando] = useState(false);
  const [lembretes, setLembretes] = useState([]);

  const [sessionId, setSessionId] = useState(() => localStorage.getItem(SESSION_KEY) || "");
  const [msgs, setMsgs] = useState([WELCOME]);
  const [reply, setReply] = useState("");
  const [streaming, setStreaming] = useState(false);
  const endRef = useRef(null);

  useEffect(() => { api.get("/lembretes/").then(({ data }) => setLembretes(data)).catch(() => {}); }, []);

  useEffect(() => {
    const inicial = localStorage.getItem(SESSION_KEY);
    if (!inicial) return;
    api.get(`/ai/chat/${inicial}/messages`)
      .then(({ data }) => { if (data.length) setMsgs(data.map((m) => ({ role: m.role, content: m.content }))); })
      .catch(() => {});
  }, []);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" }); }, [msgs]);

  const abrirWhats = () => {
    if (!numero.replace(/\D/g, "")) { toast("Informe o número do cliente", "error"); return; }
    window.open(`https://wa.me/${numero.replace(/\D/g, "")}?text=${encodeURIComponent(mensagem)}`, "_blank", "noopener,noreferrer");
    toast("Abrindo WhatsApp...", "success");
  };

  const registrar = async () => {
    if (!mensagem.trim()) { toast("Mensagem vazia", "error"); return; }
    try {
      const { data } = await api.post("/lembretes/", { mensagem, canal: numero ? `whatsapp:${numero}` : "whatsapp" });
      setLembretes((v) => [data, ...v]);
      toast("Lembrete registrado", "success");
    } catch { toast("Erro ao registrar lembrete", "error"); }
  };

  const gerarMensagem = async () => {
    setGerando(true);
    setMensagem("");
    try {
      await streamSSE("/ai/gerar-mensagem", { cliente_nome: clienteNome || null }, { onDelta: (d) => setMensagem((v) => v + d) });
      toast("Mensagem gerada pela IA", "success");
    } catch (ex) { toast(ex.message, "error"); }
    finally { setGerando(false); }
  };

  const enviar = async (e) => {
    e?.preventDefault();
    const texto = reply.trim();
    if (!texto || streaming) return;
    setReply("");
    setStreaming(true);
    setMsgs((v) => [...v, { role: "user", content: texto }, { role: "assistant", content: "", typing: true }]);
    try {
      await streamSSE("/ai/chat", { session_id: sessionId || null, message: texto }, {
        onMeta: (ev) => { if (ev.session_id && ev.session_id !== sessionId) { localStorage.setItem(SESSION_KEY, ev.session_id); setSessionId(ev.session_id); } },
        onDelta: (d) => setMsgs((v) => { const c = [...v]; const last = { ...c[c.length - 1] }; last.content += d; c[c.length - 1] = last; return c; }),
      });
    } catch (ex) {
      toast(ex.message, "error");
      setMsgs((v) => v.filter((m) => !(m.typing && !m.content)));
    } finally {
      setMsgs((v) => v.map((m) => ({ ...m, typing: false })));
      setStreaming(false);
    }
  };

  const novaConversa = () => {
    localStorage.removeItem(SESSION_KEY);
    setSessionId("");
    setMsgs([WELCOME]);
  };

  return (
    <div data-testid="atendimento-page">
      <div className="cta-inline">
        <div>
          <span className="content-eyebrow">Relacionamento</span>
          <h1 className="page-title">Atendimento inteligente</h1>
          <p className="page-sub">Central para acompanhar conversas, gerar mensagens com IA e abrir o WhatsApp em um clique.</p>
        </div>
        <div className="actions">
          <a className="btn-inline btn-wa" data-testid="btn-open-wa-top" href={`https://wa.me/${numero.replace(/\D/g, "") || ""}`} target="_blank" rel="noreferrer">
            <MessageCircle size={16} /> Abrir WhatsApp
          </a>
        </div>
      </div>

      <div className="grid-3">
        <section className="card" data-testid="card-transicao-direta">
          <span className="card-eyebrow">Transição direta</span>
          <h3>Envie um lembrete pelo WhatsApp</h3>
          <p className="desc">Digite o número do cliente e a mensagem — ou deixe a IA escrever para você.</p>

          <div className="grid-2" style={{ gap: 10 }}>
            <label className="field">
              Número (DDI + DDD)
              <input placeholder="55 42 99999-0000" value={numero} onChange={(e) => setNumero(e.target.value)} data-testid="input-numero-cliente" />
            </label>
            <label className="field">
              Nome da cliente
              <input placeholder="Ex: Amanda" value={clienteNome} onChange={(e) => setClienteNome(e.target.value)} data-testid="input-cliente-nome" />
            </label>
          </div>
          <label className="field">
            <span className="field-row">
              Mensagem
              <button type="button" className="btn-ai" onClick={gerarMensagem} disabled={gerando} data-testid="btn-gerar-mensagem-ia">
                <Sparkles size={13} /> {gerando ? "Escrevendo…" : "Gerar com IA"}
              </button>
            </span>
            <textarea rows={3} value={mensagem} onChange={(e) => setMensagem(e.target.value)} data-testid="input-mensagem" />
          </label>

          <div className="grid-2" style={{ gap: 10, marginTop: 8 }}>
            <button className="btn btn-primary" data-testid="btn-abrir-whatsapp" onClick={abrirWhats}>
              <Phone size={16} /> Abrir WhatsApp
            </button>
            <button className="btn btn-outline" data-testid="btn-registrar-lembrete" onClick={registrar}>
              <Send size={16} /> Registrar lembrete
            </button>
          </div>
        </section>

        <section className="card" data-testid="card-conversas">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
            <h3 style={{ fontSize: 18 }}>Conversas recentes</h3>
            <span className="badge rose">1 nova</span>
          </div>
          {DEMO_CONVERSAS.map((c) => (
            <div key={c.id} className={`list-item ${c.ativa ? "active" : ""}`} data-testid={`conversa-${c.id}`}>
              <div className={`avatar-sm ${c.green ? "green" : ""}`}>{c.initials}</div>
              <div className="body">
                <strong>{c.nome}</strong>
                <span className="sub">{c.ultima}</span>
              </div>
              <small className="meta">{c.hora}</small>
            </div>
          ))}
          {lembretes.length > 0 && (
            <div style={{ marginTop: 16, padding: "12px 0 0", borderTop: "1px solid var(--line)" }}>
              <span className="card-eyebrow">Lembretes registrados</span>
              {lembretes.slice(0, 3).map((l) => (
                <div key={l.id} className="list-item" data-testid={`lembrete-${l.id}`}>
                  <div className="avatar-sm">•</div>
                  <div className="body">
                    <strong style={{ fontSize: 13 }}>{l.mensagem.slice(0, 50)}{l.mensagem.length > 50 ? "…" : ""}</strong>
                    <span className="sub">{l.canal}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="card chat-card" data-testid="card-chat">
          <div className="chat-header">
            <div className="avatar-sm"><Sparkles size={16} /></div>
            <div className="body">
              <strong>Assistente ELO</strong>
              <small>Claude Sonnet 4.5 · conhece sua agenda, equipe e estoque</small>
            </div>
            <button type="button" className="topbar-icon" title="Nova conversa" onClick={novaConversa} data-testid="btn-nova-conversa">
              <RotateCcw size={15} />
            </button>
            <div className="chat-status" title="online" />
          </div>
          <div className="messages" data-testid="chat-messages">
            {msgs.map((m, i) => (
              <div key={i} className={`msg ${m.role === "user" ? "user" : "bot"} ${m.typing ? "typing" : ""}`} data-testid={`msg-${i}`}>{m.content}</div>
            ))}
            <div ref={endRef} />
          </div>
          <form className="chat-input" onSubmit={enviar}>
            <input placeholder="Pergunte sobre a agenda, clientes, estoque…" value={reply} onChange={(e) => setReply(e.target.value)} disabled={streaming} data-testid="input-reply" />
            <button type="submit" disabled={streaming || !reply.trim()} data-testid="btn-send-reply"><ArrowUp size={16} /></button>
          </form>
        </section>
      </div>

      <div style={{ marginTop: 20 }}>
        <LembretesVespera />
      </div>
    </div>
  );
}

===== FILE: frontend/src/pages/Configuracoes.jsx =====
import { useEffect, useState } from "react";
import { Plus, Trash2 } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/context/ToastContext";
import ServicoInsumos from "@/components/ServicoInsumos";

export default function Configuracoes() {
  const toast = useToast();
  const [servicos, setServicos] = useState([]);
  const [profs, setProfs] = useState([]);
  const [insumos, setInsumos] = useState([]);
  const [svForm, setSvForm] = useState({ nome: "", duracao_minutos: 30, valor: 0 });
  const [prForm, setPrForm] = useState({ nome: "", especialidades: "" });

  const load = async () => {
    const [{ data: s }, { data: p }, { data: i }] = await Promise.all([api.get("/servicos/"), api.get("/profissionais/"), api.get("/insumos/")]);
    setServicos(s); setProfs(p); setInsumos(i);
  };
  useEffect(() => { load().catch(() => toast("Erro ao carregar", "error")); /* eslint-disable-next-line */ }, []);

  const addServico = async (e) => {
    e.preventDefault();
    try {
      await api.post("/servicos/", { ...svForm, duracao_minutos: Number(svForm.duracao_minutos), valor: Number(svForm.valor) });
      toast("Serviço criado", "success");
      setSvForm({ nome: "", duracao_minutos: 30, valor: 0 }); load();
    } catch { toast("Erro", "error"); }
  };
  const delServico = async (id) => { try { await api.delete(`/servicos/${id}`); toast("Removido", "success"); load(); } catch { toast("Erro", "error"); } };
  const addProf = async (e) => {
    e.preventDefault();
    try { await api.post("/profissionais/", prForm); toast("Profissional adicionado", "success"); setPrForm({ nome: "", especialidades: "" }); load(); }
    catch { toast("Erro", "error"); }
  };
  const delProf = async (id) => { try { await api.delete(`/profissionais/${id}`); toast("Removido", "success"); load(); } catch { toast("Erro", "error"); } };

  return (
    <div data-testid="config-page">
      <div className="cta-inline">
        <div>
          <span className="content-eyebrow">Espaço de gestão</span>
          <h1 className="page-title">Configurações</h1>
          <p className="page-sub">Serviços, equipe e preferências que dão forma ao seu estúdio.</p>
        </div>
      </div>

      <div className="grid-2">
        <section className="card" data-testid="card-servicos">
          <span className="card-eyebrow">Cardápio</span>
          <h3>Serviços</h3>
          <p className="desc">Cadastre os atendimentos oferecidos e os insumos que cada um consome — o estoque baixa sozinho ao concluir.</p>
          {servicos.map((s) => (
            <div key={s.id} className="servico-block" data-testid={`servico-${s.id}`}>
              <div className="list-item">
                <div className="avatar-sm">{s.nome[0]}</div>
                <div className="body"><strong>{s.nome}</strong><span className="sub">{s.duracao_minutos} min</span></div>
                <span className="badge rose">R$ {s.valor.toFixed(2)}</span>
                <button className="topbar-icon" onClick={() => delServico(s.id)} data-testid={`btn-del-servico-${s.id}`}><Trash2 size={14} /></button>
              </div>
              <ServicoInsumos servico={s} insumos={insumos} />
            </div>
          ))}
          <form onSubmit={addServico} style={{ marginTop: 20 }}>
            <label className="field">Nome do serviço
              <input value={svForm.nome} onChange={(e) => setSvForm({ ...svForm, nome: e.target.value })} required data-testid="form-servico-nome" />
            </label>
            <div className="grid-2">
              <label className="field">Duração (min)
                <input type="number" min="1" value={svForm.duracao_minutos} onChange={(e) => setSvForm({ ...svForm, duracao_minutos: e.target.value })} data-testid="form-servico-duracao" />
              </label>
              <label className="field">Valor
                <input type="number" step="0.01" min="0" value={svForm.valor} onChange={(e) => setSvForm({ ...svForm, valor: e.target.value })} data-testid="form-servico-valor" />
              </label>
            </div>
            <button type="submit" className="btn btn-primary" data-testid="btn-add-servico"><Plus size={16} /> Adicionar serviço</button>
          </form>
        </section>

        <section className="card" data-testid="card-profissionais">
          <span className="card-eyebrow">Equipe</span>
          <h3>Profissionais</h3>
          <p className="desc">Adicione as pessoas que atendem no seu espaço.</p>
          {profs.map((p) => (
            <div key={p.id} className="list-item" data-testid={`prof-${p.id}`}>
              <div className="avatar-sm">{p.nome[0]}</div>
              <div className="body"><strong>{p.nome}</strong><span className="sub">{p.especialidades || "—"}</span></div>
              <button className="topbar-icon" onClick={() => delProf(p.id)} data-testid={`btn-del-prof-${p.id}`}><Trash2 size={14} /></button>
            </div>
          ))}
          <form onSubmit={addProf} style={{ marginTop: 20 }}>
            <label className="field">Nome
              <input value={prForm.nome} onChange={(e) => setPrForm({ ...prForm, nome: e.target.value })} required data-testid="form-prof-nome" />
            </label>
            <label className="field">Especialidades
              <input value={prForm.especialidades} onChange={(e) => setPrForm({ ...prForm, especialidades: e.target.value })} placeholder="Cabelo, Coloração" data-testid="form-prof-esp" />
            </label>
            <button type="submit" className="btn btn-primary" data-testid="btn-add-prof"><Plus size={16} /> Adicionar profissional</button>
          </form>
        </section>
      </div>
    </div>
  );
}

===== FILE: frontend/src/pages/Estoque.jsx =====
import { useEffect, useState } from "react";
import { Plus, Trash2 } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

export default function Estoque() {
  const toast = useToast();
  const [insumos, setInsumos] = useState([]);
  const [alertas, setAlertas] = useState([]);
  const [form, setForm] = useState({ nome: "", quantidade_atual: 0, quantidade_minima_alerta: 0 });

  const load = async () => {
    try {
      const [{ data: ins }, { data: al }] = await Promise.all([api.get("/insumos/"), api.get("/estoque/alertas")]);
      setInsumos(ins); setAlertas(al);
    } catch { toast("Erro ao carregar estoque", "error"); }
  };
  useEffect(() => { load(); }, []);

  const submit = async (e) => {
    e.preventDefault();
    if (!form.nome) return;
    try {
      await api.post("/insumos/", { ...form, quantidade_atual: Number(form.quantidade_atual), quantidade_minima_alerta: Number(form.quantidade_minima_alerta) });
      toast("Insumo adicionado", "success");
      setForm({ nome: "", quantidade_atual: 0, quantidade_minima_alerta: 0 });
      load();
    } catch { toast("Erro ao criar", "error"); }
  };
  const remover = async (id) => {
    try { await api.delete(`/insumos/${id}`); toast("Removido", "success"); load(); }
    catch { toast("Erro", "error"); }
  };

  return (
    <div data-testid="estoque-page">
      <div className="cta-inline">
        <div>
          <span className="content-eyebrow">Espaço de gestão</span>
          <h1 className="page-title">Estoque</h1>
          <p className="page-sub">Controle o que está saindo e o que precisa de reposição.</p>
        </div>
      </div>

      {alertas.length > 0 && (
        <section className="card" style={{ marginBottom: 20, borderLeft: "4px solid var(--gold)" }} data-testid="card-alertas">
          <span className="card-eyebrow" style={{ color: "var(--gold)" }}>Atenção</span>
          <h3>Alertas de reposição</h3>
          {alertas.map((a) => (
            <div key={a.insumo_id} className="list-item" data-testid={`alerta-${a.insumo_id}`}>
              <div className="avatar-sm">{a.nome[0]}</div>
              <div className="body"><strong>{a.nome}</strong><span className="sub">{a.mensagem}</span></div>
              <span className="badge gold">{a.tipo}</span>
            </div>
          ))}
        </section>
      )}

      <div className="grid-2">
        <section className="card" data-testid="card-insumos">
          <span className="card-eyebrow">Produtos e insumos</span>
          <h3>Inventário</h3>
          <p className="desc">{insumos.length} produto(s) em estoque.</p>
          {insumos.map((i) => (
            <div key={i.id} className="list-item" data-testid={`insumo-${i.id}`}>
              <div className="avatar-sm">{i.nome[0]}</div>
              <div className="body">
                <strong>{i.nome}</strong>
                <span className="sub">Mínimo: {i.quantidade_minima_alerta}</span>
              </div>
              <span className={`badge ${i.quantidade_atual <= i.quantidade_minima_alerta ? "red" : "green"}`}>{i.quantidade_atual} un</span>
              <button className="topbar-icon" onClick={() => remover(i.id)} data-testid={`btn-del-insumo-${i.id}`}><Trash2 size={14} /></button>
            </div>
          ))}
        </section>

        <section className="card" data-testid="card-form-insumo">
          <span className="card-eyebrow">Adicionar</span>
          <h3>Novo insumo</h3>
          <p className="desc">Cadastre um produto para acompanhar consumo e alertas.</p>
          <form onSubmit={submit}>
            <label className="field">Nome
              <input value={form.nome} onChange={(e) => setForm({ ...form, nome: e.target.value })} data-testid="form-insumo-nome" required />
            </label>
            <div className="grid-2">
              <label className="field">Quantidade atual
                <input type="number" min="0" value={form.quantidade_atual} onChange={(e) => setForm({ ...form, quantidade_atual: e.target.value })} data-testid="form-insumo-qtd" />
              </label>
              <label className="field">Mínimo
                <input type="number" min="0" value={form.quantidade_minima_alerta} onChange={(e) => setForm({ ...form, quantidade_minima_alerta: e.target.value })} data-testid="form-insumo-min" />
              </label>
            </div>
            <button type="submit" className="btn btn-primary" data-testid="btn-add-insumo"><Plus size={16} /> Adicionar</button>
          </form>
        </section>
      </div>
    </div>
  );
}

===== FILE: frontend/src/pages/Financeiro.jsx =====
import { useEffect, useState } from "react";
import { Plus, TrendingUp, TrendingDown } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

export default function Financeiro() {
  const toast = useToast();
  const [resumo, setResumo] = useState({ entradas: 0, saidas: 0, saldo: 0, lancamentos: [] });
  const [form, setForm] = useState({ tipo: "entrada", valor: 0, descricao: "" });

  const load = async () => {
    try { const { data } = await api.get("/financeiro/resumo"); setResumo(data); }
    catch { toast("Erro ao carregar financeiro", "error"); }
  };
  useEffect(() => { load(); }, []);

  const submit = async (e) => {
    e.preventDefault();
    if (!form.descricao || !form.valor) return;
    try {
      await api.post("/financeiro/lancamentos", { ...form, valor: Number(form.valor) });
      toast("Lançamento registrado", "success");
      setForm({ tipo: "entrada", valor: 0, descricao: "" });
      load();
    } catch { toast("Erro ao criar", "error"); }
  };

  return (
    <div data-testid="financeiro-page">
      <div className="cta-inline">
        <div>
          <span className="content-eyebrow">Espaço de gestão</span>
          <h1 className="page-title">Financeiro</h1>
          <p className="page-sub">Um panorama simples do que entra e o que sai do seu espaço.</p>
        </div>
      </div>

      <div className="finance-hero" data-testid="finance-hero">
        <span className="lbl">Saldo do período</span>
        <span className="val">R$ {resumo.saldo.toFixed(2)}</span>
        <span className="sub">{resumo.lancamentos.length} lançamento(s) registrados</span>
        <div className="fin-summary">
          <div><span className="k">Entradas</span><span className="v">R$ {resumo.entradas.toFixed(2)}</span></div>
          <div><span className="k">Saídas</span><span className="v">R$ {resumo.saidas.toFixed(2)}</span></div>
          <div><span className="k">Saldo</span><span className="v">R$ {resumo.saldo.toFixed(2)}</span></div>
        </div>
      </div>

      <div className="grid-2" style={{ marginTop: 20 }}>
        <section className="card" data-testid="card-lancamentos">
          <span className="card-eyebrow">Últimos movimentos</span>
          <h3>Lançamentos</h3>
          <p className="desc">Histórico de entradas e saídas.</p>
          {resumo.lancamentos.length === 0 && <div className="empty"><h4>Sem movimentos</h4><p>Comece adicionando o primeiro lançamento.</p></div>}
          {resumo.lancamentos.map((l) => (
            <div key={l.id} className="list-item" data-testid={`lanc-${l.id}`}>
              <div className={`avatar-sm ${l.tipo === "entrada" ? "green" : ""}`}>
                {l.tipo === "entrada" ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
              </div>
              <div className="body">
                <strong>{l.descricao}</strong>
                <span className="sub">{new Date(l.data).toLocaleString("pt-BR")}</span>
              </div>
              <span className={`badge ${l.tipo === "entrada" ? "green" : "red"}`}>
                {l.tipo === "entrada" ? "+" : "-"} R$ {l.valor.toFixed(2)}
              </span>
            </div>
          ))}
        </section>

        <section className="card" data-testid="card-form-lanc">
          <span className="card-eyebrow">Novo lançamento</span>
          <h3>Registrar movimento</h3>
          <p className="desc">Adicione entradas de atendimentos ou saídas de compras.</p>
          <form onSubmit={submit}>
            <label className="field">Tipo
              <select value={form.tipo} onChange={(e) => setForm({ ...form, tipo: e.target.value })} data-testid="form-lanc-tipo">
                <option value="entrada">Entrada</option>
                <option value="saida">Saída</option>
              </select>
            </label>
            <label className="field">Descrição
              <input value={form.descricao} onChange={(e) => setForm({ ...form, descricao: e.target.value })} data-testid="form-lanc-desc" required />
            </label>
            <label className="field">Valor
              <input type="number" step="0.01" min="0" value={form.valor} onChange={(e) => setForm({ ...form, valor: e.target.value })} data-testid="form-lanc-valor" required />
            </label>
            <button type="submit" className="btn btn-primary" data-testid="btn-add-lanc"><Plus size={16} /> Registrar</button>
          </form>
        </section>
      </div>
    </div>
  );
}

===== FILE: frontend/src/pages/Landing.jsx =====
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Search, X } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useToast } from "@/context/ToastContext";

const GoogleMark = () => (
  <svg width="18" height="18" viewBox="0 0 48 48" aria-hidden="true">
    <path fill="#EA4335" d="M24 9.5c3.5 0 6.6 1.2 9.1 3.6l6.8-6.8C35.8 2.4 30.3 0 24 0 14.6 0 6.5 5.4 2.6 13.2l7.9 6.1C12.4 13.6 17.7 9.5 24 9.5z" />
    <path fill="#4285F4" d="M46.5 24.5c0-1.6-.1-2.8-.4-4H24v8.1h12.9c-.3 2.2-1.7 5.4-4.9 7.6l7.6 5.9c4.5-4.2 6.9-10.3 6.9-17.6z" />
    <path fill="#FBBC05" d="M10.5 28.7A14.6 14.6 0 0 1 9.7 24c0-1.6.3-3.2.8-4.7l-7.9-6.1A24 24 0 0 0 0 24c0 3.9.9 7.5 2.6 10.8l7.9-6.1z" />
    <path fill="#34A853" d="M24 48c6.5 0 11.9-2.1 15.9-5.8l-7.6-5.9c-2 1.4-4.7 2.4-8.3 2.4-6.3 0-11.6-4.1-13.5-9.9l-7.9 6.1C6.5 42.6 14.6 48 24 48z" />
  </svg>
);

export default function Landing() {
  const [mode, setMode] = useState(null); // null | "login" | "register"
  const [form, setForm] = useState({ nome: "", email: "admin@elo.beauty", senha: "elo123456", business: "" });
  const [err, setErr] = useState("");
  const [busy, setBusy] = useState(false);
  const { login, register, loginWithGoogle } = useAuth();
  const nav = useNavigate();
  const toast = useToast();

  const open = (m) => {
    setErr("");
    setForm(m === "login" ? { nome: "", email: "admin@elo.beauty", senha: "elo123456", business: "" } : { nome: "", email: "", senha: "", business: "" });
    setMode(m);
  };
  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value });

  const submit = async (e) => {
    e.preventDefault();
    setErr(""); setBusy(true);
    try {
      if (mode === "login") {
        await login(form.email, form.senha);
        toast("Bem-vinda de volta", "success");
      } else {
        await register({ nome: form.nome, email: form.email, senha: form.senha, business: form.business || null });
        toast("Conta criada com sucesso", "success");
      }
      nav("/app/atendimento");
    } catch (ex) {
      const detail = ex.response?.data?.detail;
      setErr(typeof detail === "string" ? detail : mode === "login" ? "Credenciais inválidas. Tente admin@elo.beauty / elo123456." : "Não foi possível criar a conta.");
    } finally { setBusy(false); }
  };

  const isLogin = mode === "login";

  return (
    <div className="landing">
      <div className="landing-hero" data-testid="landing-hero">
        <span className="landing-eyebrow">Gestão para salões</span>
        <h1>Seu cuidado,<br /><em>organizado.</em></h1>
        <p>Uma visão mais simples e bonita para cuidar do seu negócio todos os dias.</p>
      </div>

      <div className="landing-panel">
        <div className="brand">
          <span className="brand-mark">ELO</span>
          <span className="brand-tagline">beauty care</span>
        </div>

        <span className="panel-eyebrow">Bem-vinda de volta</span>
        <h2>Gerencie seu espaço</h2>
        <p className="lead">Entre para acompanhar sua agenda, equipe e resultados.</p>

        <div className="search-input" data-testid="landing-search">
          <Search size={18} />
          <input placeholder="Buscar serviços" />
        </div>

        <div className="btn-stack">
          <button type="button" className="btn btn-primary" data-testid="btn-enter-platform" onClick={() => open("login")}>
            Entrar na plataforma
          </button>
          <button type="button" className="btn btn-google" data-testid="btn-google-login" onClick={loginWithGoogle}>
            <GoogleMark /> Continuar com Google
          </button>
          <button type="button" className="btn btn-outline" data-testid="btn-create-account" onClick={() => open("register")}>
            Criar uma conta
          </button>
        </div>

        <div className="landing-footer">
          <span>Disponível para seu time</span>
          <span><strong>Google Play</strong> · <strong>App Store</strong></span>
        </div>
      </div>

      {mode && (
        <div className="modal-backdrop" role="dialog" data-testid="login-modal" onClick={(e) => e.target === e.currentTarget && setMode(null)}>
          <form className="modal-card" onSubmit={submit}>
            <div className="modal-header">
              <span className="modal-eyebrow">{isLogin ? "Acesso seguro" : "Novo espaço"}</span>
              <button type="button" className="modal-close" data-testid="login-modal-close" onClick={() => setMode(null)}>
                <X size={20} />
              </button>
            </div>
            <h3>{isLogin ? "Continue com seu e-mail" : "Crie sua conta"}</h3>
            <p className="hint">{isLogin ? "Seus dados ficam protegidos e ligados ao seu espaço." : "Leva menos de um minuto para começar a organizar seu salão."}</p>

            {!isLogin && (
              <>
                <label className="field">
                  <input value={form.nome} onChange={set("nome")} placeholder="Seu nome" data-testid="register-nome" required />
                </label>
                <label className="field">
                  <input value={form.business} onChange={set("business")} placeholder="Nome do espaço (opcional)" data-testid="register-business" />
                </label>
              </>
            )}
            <label className="field">
              <input type="email" value={form.email} onChange={set("email")} placeholder="seu@email.com" data-testid="login-email" required />
            </label>
            <label className="field">
              <input type="password" value={form.senha} onChange={set("senha")} placeholder="••••••••••" data-testid="login-password" minLength={6} required />
            </label>
            <button className="btn btn-primary" type="submit" disabled={busy} data-testid="login-submit">
              {busy ? "Aguarde..." : isLogin ? "Confirmar acesso" : "Criar conta"}
            </button>
            {err && <div className="modal-error" data-testid="login-error">{err}</div>}

            <div className="auth-divider">ou</div>
            <button type="button" className="btn btn-google" data-testid="modal-google-login" onClick={loginWithGoogle}>
              <GoogleMark /> Continuar com Google
            </button>
            <p className="auth-switch">
              {isLogin ? "Ainda não tem conta?" : "Já tem uma conta?"}{" "}
              <button type="button" data-testid="auth-switch-mode" onClick={() => open(isLogin ? "register" : "login")}>
                {isLogin ? "Criar agora" : "Entrar"}
              </button>
            </p>
          </form>
        </div>
      )}
    </div>
  );
}

===== FILE: frontend/src/pages/Perfil.jsx =====
import { useEffect, useState } from "react";
import { Save } from "lucide-react";
import { useAuth } from "@/context/AuthContext";
import { useToast } from "@/context/ToastContext";

export default function Perfil() {
  const { user, updateProfile } = useAuth();
  const toast = useToast();
  const [form, setForm] = useState({ nome: "", email: "", business: "", city: "" });

  useEffect(() => {
    if (user) setForm({ nome: user.nome || "", email: user.email || "", business: user.business || "", city: user.city || "" });
  }, [user]);

  const submit = async (e) => {
    e.preventDefault();
    try { await updateProfile(form); toast("Perfil atualizado", "success"); }
    catch { toast("Erro ao atualizar", "error"); }
  };

  const initials = (form.nome || "AE").split(" ").map((n) => n[0]).slice(0,2).join("").toUpperCase();

  return (
    <div data-testid="perfil-page">
      <div className="cta-inline">
        <div>
          <span className="content-eyebrow">Espaço de gestão</span>
          <h1 className="page-title">Perfil</h1>
          <p className="page-sub">Personalize sua identidade profissional e do estúdio.</p>
        </div>
      </div>

      <div className="grid-2">
        <section className="card" style={{ textAlign: "center", padding: 40 }} data-testid="card-perfil-hero">
          <div style={{ width: 96, height: 96, borderRadius: "50%", background: "var(--wine)", color: "#fff", display: "grid", placeItems: "center", fontFamily: "'Playfair Display', serif", fontSize: 34, fontWeight: 600, margin: "0 auto 16px", border: "6px solid var(--rose-soft)" }}>
            {initials}
          </div>
          <h3 style={{ fontSize: 26 }}>{form.nome || "Sem nome"}</h3>
          <p style={{ color: "var(--muted)", fontSize: 14, marginTop: 4 }}>{form.business || "Espaço próprio"}</p>
          <p style={{ color: "var(--muted)", fontSize: 12, marginTop: 12 }}>📍 {form.city || "—"}</p>
          <div style={{ marginTop: 20, display: "flex", justifyContent: "center", gap: 12 }}>
            <span className="badge green">● Online</span>
            <span className="badge rose">ELO Beauty</span>
          </div>
        </section>

        <section className="card" data-testid="card-perfil-form">
          <span className="card-eyebrow">Detalhes</span>
          <h3>Informações pessoais</h3>
          <p className="desc">Atualize seus dados de exibição no espaço.</p>
          <form onSubmit={submit}>
            <label className="field">Nome
              <input value={form.nome} onChange={(e) => setForm({ ...form, nome: e.target.value })} data-testid="form-perfil-nome" />
            </label>
            <label className="field">E-mail
              <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} data-testid="form-perfil-email" />
            </label>
            <label className="field">Nome do espaço
              <input value={form.business} onChange={(e) => setForm({ ...form, business: e.target.value })} data-testid="form-perfil-business" />
            </label>
            <label className="field">Cidade
              <input value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} data-testid="form-perfil-city" />
            </label>
            <button type="submit" className="btn btn-primary" data-testid="btn-save-perfil"><Save size={16} /> Salvar alterações</button>
          </form>
        </section>
      </div>
    </div>
  );
}

===== FILE: frontend/tailwind.config.js =====
/** @type {import('tailwindcss').Config} */
module.exports = {
    // `overline` is a Tailwind utility; without this an app's own eyebrow-label class draws a line above the text.
    blocklist: ["overline"],
    darkMode: ["class"],
    content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      borderRadius: {
        lg: 'var(--radius)',
        md: 'calc(var(--radius) - 2px)',
        sm: 'calc(var(--radius) - 4px)'
      },
      colors: {
        background: 'hsl(var(--background))',
        foreground: 'hsl(var(--foreground))',
        card: {
          DEFAULT: 'hsl(var(--card))',
          foreground: 'hsl(var(--card-foreground))'
        },
        popover: {
          DEFAULT: 'hsl(var(--popover))',
          foreground: 'hsl(var(--popover-foreground))'
        },
        primary: {
          DEFAULT: 'hsl(var(--primary))',
          foreground: 'hsl(var(--primary-foreground))'
        },
        secondary: {
          DEFAULT: 'hsl(var(--secondary))',
          foreground: 'hsl(var(--secondary-foreground))'
        },
        muted: {
          DEFAULT: 'hsl(var(--muted))',
          foreground: 'hsl(var(--muted-foreground))'
        },
        accent: {
          DEFAULT: 'hsl(var(--accent))',
          foreground: 'hsl(var(--accent-foreground))'
        },
        destructive: {
          DEFAULT: 'hsl(var(--destructive))',
          foreground: 'hsl(var(--destructive-foreground))'
        },
        border: 'hsl(var(--border))',
        input: 'hsl(var(--input))',
        ring: 'hsl(var(--ring))',
        chart: {
          '1': 'hsl(var(--chart-1))',
          '2': 'hsl(var(--chart-2))',
          '3': 'hsl(var(--chart-3))',
          '4': 'hsl(var(--chart-4))',
          '5': 'hsl(var(--chart-5))'
        }
      },
      keyframes: {
        'accordion-down': {
          from: {
            height: '0'
          },
          to: {
            height: 'var(--radix-accordion-content-height)'
          }
        },
        'accordion-up': {
          from: {
            height: 'var(--radix-accordion-content-height)'
          },
          to: {
            height: '0'
          }
        }
      },
      animation: {
        'accordion-down': 'accordion-down 0.2s ease-out',
        'accordion-up': 'accordion-up 0.2s ease-out'
      }
    }
  },
  plugins: [require("tailwindcss-animate")],
};
===== FILE: .vscode/extensions.json =====
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "ms-python.debugpy",
    "dbaeumer.vscode-eslint",
    "esbenp.prettier-vscode",
    "bradlc.vscode-tailwindcss",
    "mongodb.mongodb-vscode",
    "dsznajder.es7-react-js-snippets"
  ]
}

===== FILE: .vscode/launch.json =====
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Backend: FastAPI (uvicorn)",
      "type": "debugpy",
      "request": "launch",
      "module": "uvicorn",
      "args": ["server:app", "--reload", "--host", "0.0.0.0", "--port", "8001"],
      "cwd": "${workspaceFolder}/backend",
      "envFile": "${workspaceFolder}/backend/.env",
      "jinja": true,
      "justMyCode": true
    },
    {
      "name": "Frontend: React (yarn start)",
      "type": "node-terminal",
      "request": "launch",
      "command": "yarn start",
      "cwd": "${workspaceFolder}/frontend"
    },
    {
      "name": "Frontend: Chrome (attach em localhost:3000)",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:3000",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ],
  "compounds": [
    {
      "name": "Full stack (backend + frontend)",
      "configurations": ["Backend: FastAPI (uvicorn)", "Frontend: React (yarn start)"],
      "stopAll": true
    }
  ]
}

===== FILE: .vscode/settings.json =====
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/.venv/bin/python",
  "python.analysis.extraPaths": ["${workspaceFolder}/backend"],
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["backend"],
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.formatOnSave": true
  },
  "[javascript]": { "editor.defaultFormatter": "esbenp.prettier-vscode", "editor.formatOnSave": true },
  "[javascriptreact]": { "editor.defaultFormatter": "esbenp.prettier-vscode", "editor.formatOnSave": true },
  "[css]": { "editor.defaultFormatter": "esbenp.prettier-vscode" },
  "eslint.workingDirectories": ["frontend"],
  "tailwindCSS.experimental.configFile": "frontend/tailwind.config.js",
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/.ruff_cache": true,
    "**/node_modules": true
  },
  "search.exclude": {
    "**/node_modules": true,
    "**/yarn.lock": true,
    "**/test_reports": true
  }
}

'''


if __name__ == "__main__":
    main()
