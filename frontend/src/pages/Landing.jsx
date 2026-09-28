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
