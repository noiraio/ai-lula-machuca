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
