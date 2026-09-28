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
