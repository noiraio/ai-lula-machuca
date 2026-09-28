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
