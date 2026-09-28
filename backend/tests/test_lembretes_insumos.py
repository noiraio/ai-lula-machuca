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
