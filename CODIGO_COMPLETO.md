# ELO Beauty Care — Código completo (por arquivo)

Cada seção abaixo é **um arquivo**: crie o arquivo no caminho indicado dentro do VS Code e cole o conteúdo do bloco.

Ordem sugerida: raiz → backend → frontend. Depois siga o `README.md` para rodar.

> A seção 7 traz `package.json`, `craco.config.js` e `public/index.html` em **versão local simplificada** (sem plugins da plataforma). Componentes `shadcn/ui`, `tailwind` e `constants/testIds` não são usados pelo app e foram omitidos.


## Índice

- **1. Raiz do projeto**: `README.md`, `INTEGRACAO_WHATSAPP.md`, `.gitignore`, `.vscode/launch.json`, `.vscode/settings.json`, `.vscode/extensions.json`
- **2. Backend — configuração**: `backend/requirements.txt`, `backend/.env.example`, `backend/pytest.ini`, `backend/server.py`
- **3. Backend — app/ (núcleo)**: `backend/app/__init__.py`, `backend/app/config.py`, `backend/app/db.py`, `backend/app/crud.py`, `backend/app/dependencies.py`
- **4. Backend — app/schemas/**: `backend/app/schemas/__init__.py`, `backend/app/schemas/usuario.py`, `backend/app/schemas/agendamento.py`, `backend/app/schemas/servico.py`, `backend/app/schemas/insumo.py`, `backend/app/schemas/profissional.py`, `backend/app/schemas/estoque.py`, `backend/app/schemas/financeiro.py`, `backend/app/schemas/debito.py`, `backend/app/schemas/lembrete.py`, `backend/app/schemas/ai.py`
- **5. Backend — app/services/**: `backend/app/services/__init__.py`, `backend/app/services/auth.py`, `backend/app/services/ai.py`, `backend/app/services/lembretes.py`, `backend/app/services/whatsapp.py`
- **6. Backend — app/routers/**: `backend/app/routers/__init__.py`, `backend/app/routers/auth.py`, `backend/app/routers/agendamentos.py`, `backend/app/routers/servicos.py`, `backend/app/routers/insumos.py`, `backend/app/routers/profissionais.py`, `backend/app/routers/estoque.py`, `backend/app/routers/financeiro.py`, `backend/app/routers/dashboard.py`, `backend/app/routers/debitos.py`, `backend/app/routers/lembretes.py`, `backend/app/routers/ai.py`
- **7. Frontend — configuração (versão local simplificada)**: `frontend/package.json`, `frontend/craco.config.js`, `frontend/jsconfig.json`, `frontend/.env.example`, `frontend/.gitignore`, `frontend/public/index.html`
- **8. Frontend — src/ (núcleo)**: `frontend/src/index.js`, `frontend/src/App.js`, `frontend/src/App.css`, `frontend/src/index.css`, `frontend/src/lib/api.js`, `frontend/src/context/AuthContext.jsx`, `frontend/src/context/ToastContext.jsx`
- **9. Frontend — src/components/**: `frontend/src/components/AppShell.jsx`, `frontend/src/components/AuthCallback.jsx`, `frontend/src/components/LembretesVespera.jsx`, `frontend/src/components/ServicoInsumos.jsx`
- **10. Frontend — src/pages/**: `frontend/src/pages/Landing.jsx`, `frontend/src/pages/Atendimento.jsx`, `frontend/src/pages/Agenda.jsx`, `frontend/src/pages/Estoque.jsx`, `frontend/src/pages/Financeiro.jsx`, `frontend/src/pages/Perfil.jsx`, `frontend/src/pages/Configuracoes.jsx`

---


## 1. Raiz do projeto

### 📄 `README.md`

```markdown
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
```

### 📄 `INTEGRACAO_WHATSAPP.md`

```markdown
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
```

### 📄 `.gitignore`

```text
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
```

### 📄 `.vscode/launch.json`

```json
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
```

### 📄 `.vscode/settings.json`

```json
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
```

### 📄 `.vscode/extensions.json`

```json
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
```


## 2. Backend — configuração

### 📄 `backend/requirements.txt`

```text
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
```

### 📄 `backend/.env.example`

```bash
MONGO_URL="mongodb://localhost:27017"
DB_NAME="elo_beauty"
CORS_ORIGINS="*"
SECRET_KEY="troque-por-um-segredo-longo-e-aleatorio"
EMERGENT_LLM_KEY="sk-emergent-sua-chave"
APP_TIMEZONE="America/Sao_Paulo"
TWILIO_ACCOUNT_SID=""
TWILIO_AUTH_TOKEN=""
TWILIO_WHATSAPP_FROM="whatsapp:+14155238886"
```

### 📄 `backend/pytest.ini`

```ini
[pytest]
# Fixed 2 xdist workers (deterministic, not reliant on the agent passing -n). loadscope pins each test
# class/module to one worker — generated suites share one preview backend and assume sequential shared
# state — so it parallelizes across classes/modules without cross-test races.
# AGENT: do NOT modify addopts; keep exactly -n 2 --dist loadscope and run only what is configured here.
# Serial = `-n 0` (NOT `-p no:xdist`, which errors because addopts still passes -n/--dist). A custom `-n`
# option in your own pytest setup collides with xdist's -n — rename it.
required_plugins = pytest-xdist
addopts = -n 2 --dist loadscope
```

### 📄 `backend/server.py`

```python
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
```


## 3. Backend — app/ (núcleo)

### 📄 `backend/app/__init__.py`

```python

```

### 📄 `backend/app/config.py`

```python
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
```

### 📄 `backend/app/db.py`

```python
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
```

### 📄 `backend/app/crud.py`

```python
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
```

### 📄 `backend/app/dependencies.py`

```python
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
```


## 4. Backend — app/schemas/

### 📄 `backend/app/schemas/__init__.py`

```python

```

### 📄 `backend/app/schemas/usuario.py`

```python
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
```

### 📄 `backend/app/schemas/agendamento.py`

```python
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
```

### 📄 `backend/app/schemas/servico.py`

```python
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
```

### 📄 `backend/app/schemas/insumo.py`

```python
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
```

### 📄 `backend/app/schemas/profissional.py`

```python
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
```

### 📄 `backend/app/schemas/estoque.py`

```python
from pydantic import BaseModel


class AlertaEstoqueResponse(BaseModel):
    insumo_id: str
    nome: str
    quantidade_atual: float
    quantidade_minima_alerta: float
    demanda_prevista: float
    tipo: str
    mensagem: str
```

### 📄 `backend/app/schemas/financeiro.py`

```python
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
```

### 📄 `backend/app/schemas/debito.py`

```python
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
```

### 📄 `backend/app/schemas/lembrete.py`

```python
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
```

### 📄 `backend/app/schemas/ai.py`

```python
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
```


## 5. Backend — app/services/

### 📄 `backend/app/services/__init__.py`

```python

```

### 📄 `backend/app/services/auth.py`

```python
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
```

### 📄 `backend/app/services/ai.py`

```python
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
```

### 📄 `backend/app/services/lembretes.py`

```python
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
```

### 📄 `backend/app/services/whatsapp.py`

```python
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
```


## 6. Backend — app/routers/

### 📄 `backend/app/routers/__init__.py`

```python

```

### 📄 `backend/app/routers/auth.py`

```python
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
```

### 📄 `backend/app/routers/agendamentos.py`

```python
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
```

### 📄 `backend/app/routers/servicos.py`

```python
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
```

### 📄 `backend/app/routers/insumos.py`

```python
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
```

### 📄 `backend/app/routers/profissionais.py`

```python
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
```

### 📄 `backend/app/routers/estoque.py`

```python
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
```

### 📄 `backend/app/routers/financeiro.py`

```python
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
```

### 📄 `backend/app/routers/dashboard.py`

```python
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
```

### 📄 `backend/app/routers/debitos.py`

```python
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
```

### 📄 `backend/app/routers/lembretes.py`

```python
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
```

### 📄 `backend/app/routers/ai.py`

```python
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
```


## 7. Frontend — configuração (versão local simplificada)

### 📄 `frontend/package.json`

```json
{
  "name": "elo-beauty-care-frontend",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "start": "craco start",
    "build": "craco build",
    "test": "craco test"
  },
  "dependencies": {
    "@tanstack/react-query": "5.56.2",
    "axios": "1.18.0",
    "lucide-react": "0.516.0",
    "react": "19.0.0",
    "react-dom": "19.0.0",
    "react-router-dom": "7.15.0",
    "react-scripts": "5.0.1"
  },
  "devDependencies": {
    "@craco/craco": "7.1.0"
  },
  "browserslist": {
    "production": [">0.2%", "not dead", "not op_mini all"],
    "development": ["last 1 chrome version", "last 1 firefox version", "last 1 safari version"]
  }
}
```

### 📄 `frontend/craco.config.js`

```javascript
const path = require("path");

module.exports = {
  webpack: {
    alias: { "@": path.resolve(__dirname, "src") },
  },
};
```

### 📄 `frontend/jsconfig.json`

```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"]
    }
  },
  "include": ["src"]
}
```

### 📄 `frontend/.env.example`

```bash
REACT_APP_BACKEND_URL=http://localhost:8001
```

### 📄 `frontend/.gitignore`

```text
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
```

### 📄 `frontend/public/index.html`

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="theme-color" content="#6b1f2e" />
    <meta name="description" content="ELO Beauty Care — gestão inteligente para salões de beleza" />
    <title>ELO Beauty Care</title>
  </head>
  <body>
    <noscript>Você precisa habilitar o JavaScript para usar o ELO Beauty Care.</noscript>
    <div id="root"></div>
  </body>
</html>
```


## 8. Frontend — src/ (núcleo)

### 📄 `frontend/src/index.js`

```javascript
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
```

### 📄 `frontend/src/App.js`

```javascript
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
```

### 📄 `frontend/src/App.css`

```css
/* App-level styles are in index.css */
.App { min-height: 100vh; }
```

### 📄 `frontend/src/index.css`

```css
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
```

### 📄 `frontend/src/lib/api.js`

```javascript
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
```

### 📄 `frontend/src/context/AuthContext.jsx`

```jsx
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
```

### 📄 `frontend/src/context/ToastContext.jsx`

```jsx
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
```


## 9. Frontend — src/components/

### 📄 `frontend/src/components/AppShell.jsx`

```jsx
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
```

### 📄 `frontend/src/components/AuthCallback.jsx`

```jsx
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
```

### 📄 `frontend/src/components/LembretesVespera.jsx`

```jsx
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
```

### 📄 `frontend/src/components/ServicoInsumos.jsx`

```jsx
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
```


## 10. Frontend — src/pages/

### 📄 `frontend/src/pages/Landing.jsx`

```jsx
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
```

### 📄 `frontend/src/pages/Atendimento.jsx`

```jsx
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
```

### 📄 `frontend/src/pages/Agenda.jsx`

```jsx
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
```

### 📄 `frontend/src/pages/Estoque.jsx`

```jsx
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
```

### 📄 `frontend/src/pages/Financeiro.jsx`

```jsx
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
```

### 📄 `frontend/src/pages/Perfil.jsx`

```jsx
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
```

### 📄 `frontend/src/pages/Configuracoes.jsx`

```jsx
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
```
