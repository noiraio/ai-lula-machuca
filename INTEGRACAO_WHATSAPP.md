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
