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
