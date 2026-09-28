import { useEffect, useState } from "react";
import { Plus, Trash2 } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

export default function Configuracoes() {
  const toast = useToast();
  const [servicos, setServicos] = useState([]);
  const [profs, setProfs] = useState([]);
  const [svForm, setSvForm] = useState({ nome: "", duracao_minutos: 30, valor: 0 });
  const [prForm, setPrForm] = useState({ nome: "", especialidades: "" });

  const load = async () => {
    const [{ data: s }, { data: p }] = await Promise.all([api.get("/servicos/"), api.get("/profissionais/")]);
    setServicos(s); setProfs(p);
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
          <p className="desc">Cadastre os atendimentos oferecidos.</p>
          {servicos.map((s) => (
            <div key={s.id} className="list-item" data-testid={`servico-${s.id}`}>
              <div className="avatar-sm">{s.nome[0]}</div>
              <div className="body"><strong>{s.nome}</strong><span className="sub">{s.duracao_minutos} min</span></div>
              <span className="badge rose">R$ {s.valor.toFixed(2)}</span>
              <button className="topbar-icon" onClick={() => delServico(s.id)} data-testid={`btn-del-servico-${s.id}`}><Trash2 size={14} /></button>
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
