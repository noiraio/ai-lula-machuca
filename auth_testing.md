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
