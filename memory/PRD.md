# ELO Beauty Care — PRD

## Problema original
Reescrever o frontend do projeto `beleza-integrada` com o visual do protótipo `elo-beauty-care` (HTML/CSS/JS) em React, conectado ao backend FastAPI existente, mantendo MongoDB, autenticação JWT (admin@elo.beauty) + login social Google, e telas Agenda, Perfil, Atendimento, Estoque, Financeiro e Configurações. Adicionar IA (Claude Sonnet 4.5).

## Decisões do usuário
- Stack: React + FastAPI + MongoDB (Motor)
- Auth: JWT (e-mail/senha) + Google via Emergent-managed Auth
- IA: Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`) usando a **chave universal Emergent** (usuário mudou de "chave própria" para Emergent em 2026-06)
- Escopo de IA escolhido (opção b): chat do Atendimento (multi-turno, histórico) + "Gerar mensagem com IA" para lembrete WhatsApp
- Idioma: Português

## Arquitetura
```
backend/
  server.py            FastAPI, CORS (credentials), seed idempotente, /api/*
  app/config.py        env (MONGO_URL, DB_NAME, SECRET_KEY, EMERGENT_LLM_KEY, CORS_ORIGINS)
  app/db.py            Motor client, PyObjectId, BaseDocument (from_mongo/to_mongo), oid(), utc()
  app/crud.py          helpers CRUD genéricos (listar/criar/obter/atualizar/deletar)
  app/dependencies.py  get_current_user: Bearer JWT | Bearer session_token | cookie session_token
  app/services/auth.py bcrypt + JWT
  app/services/ai.py   LlmChat (anthropic/claude-sonnet-4-5-20250929), contexto do salão, prompt WhatsApp (véspera)
  app/services/whatsapp.py  Twilio WhatsApp (REST/httpx), opcional via TWILIO_* — normalizar_telefone, link_wa, enviar
  app/services/lembretes.py agendamentos de amanhã, salvar mensagem, registrar envio/erro
  app/routers/         auth, agendamentos, servicos, insumos, profissionais, dashboard, estoque, financeiro, debitos, lembretes, ai
  app/schemas/         pydantic (Response models extendem BaseDocument, id: str)
frontend/src/
  App.js               AppRouter (detecta #session_id → AuthCallback), rotas protegidas
  context/AuthContext  login, register, loginWithGoogle, processSession, logout, updateProfile
  components/AuthCallback.jsx, AppShell.jsx
  lib/api.js           axios (withCredentials) + streamSSE()
  pages/               Landing, Atendimento (chat IA + gerar mensagem), Agenda, Estoque, Financeiro, Perfil, Configuracoes
```

## Coleções MongoDB
usuarios, user_sessions, clientes, profissionais, servicos, insumos, servico_insumos, agendamentos, movimentos_financeiros, debitos, lembretes, chat_messages

## Endpoints principais (/api)
- auth: POST login, POST register, POST session (Google), POST logout, GET/PUT me
- agendamentos: GET(list/filtros), POST, PUT/{id}, PATCH/{id}/concluir, DELETE/{id}
- servicos/insumos/profissionais: CRUD completo
- estoque/alertas, financeiro/resumo, financeiro/lancamentos, dashboard/financeiro, lembretes, debitos
- ai: POST chat (SSE), GET chat/{session_id}/messages, POST gerar-mensagem (SSE)

## Implementado
- 2026-06 (sessão anterior): port do backend, esqueleto React com visual ELO — *porém DB foi migrado indevidamente para SQLite*
- 2026-06 (esta sessão):
  - Revertido backend para **MongoDB** (removido SQLAlchemy/aiosqlite), IDs string, datas UTC com Z
  - Registro de conta (/auth/register) + modal login/cadastro na Landing
  - **Google Auth Emergent-managed** (session exchange no backend, cookie httpOnly + Bearer, user_sessions com TTL)
  - **Claude Sonnet 4.5** via chave Emergent: chat do Assistente ELO com contexto real (agenda de hoje, serviços, equipe, estoque baixo), streaming SSE, histórico persistido por sessão; botão "Gerar com IA" no lembrete WhatsApp
  - Testes: iteration_1 — 26/26 backend + todos fluxos frontend OK
- 2026-06 (sessão 3):
  - **Confirmação automática** — card "Lembretes de amanhã" no Atendimento: lista agendamentos de amanhã (fuso `APP_TIMEZONE`), "Gerar todas com IA" (SSE paralelo, 3 simultâneas), mensagem editável, envio via wa.me (marca enviado + registra em `lembretes`) e envio automático **Twilio** (opcional: ativa ao preencher `TWILIO_*` no .env; sem chaves → 503 + botões desabilitados + aviso). Módulo isolado `services/whatsapp.py` + guia `INTEGRACAO_WHATSAPP.md`
  - **Insumos por serviço** — Configurações: seção expansível por serviço (vincular/upsert/remover `servico_insumos`); concluir agendamento deduz estoque (409 se insuficiente, não deduz 2x) e mostra toasts de alerta; alertas de demanda no Estoque ativos; quantidades de insumo aceitam decimais
  - Testes: iteration_2 — 17/17 backend + frontend OK

## Backlog
- P1: IA nas demais telas (Resumo do dia na Agenda, Análise de reposição no Estoque, Insights no Financeiro, bio no Perfil, sugestão de serviços em Configurações) — proposto, usuário optou por começar só pelo Atendimento
- P1: "Conversas recentes" no Atendimento ainda é conteúdo DEMO estático do protótipo
- P1: Usuário preencher credenciais Twilio (`TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_WHATSAPP_FROM`) para ativar envio automático
- P2: agendar disparo automático dos lembretes de véspera (cron diário) — hoje é "um clique"
- P2: débitos na tela Financeiro (endpoint existe, sem UI)
- P2: busca global (topbar ⌘K) e botão de ajuda ainda decorativos
