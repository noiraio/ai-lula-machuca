import { useEffect, useState } from "react";
import { Plus, TrendingUp, TrendingDown } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

export default function Financeiro() {
  const toast = useToast();
  const [resumo, setResumo] = useState({ entradas: 0, saidas: 0, saldo: 0, lancamentos: [] });
  const [form, setForm] = useState({ tipo: "entrada", valor: 0, descricao: "" });

  const load = async () => {
    try { const { data } = await api.get("/financeiro/resumo"); setResumo(data); }
    catch { toast("Erro ao carregar financeiro", "error"); }
  };
  useEffect(() => { load(); }, []);

  const submit = async (e) => {
    e.preventDefault();
    if (!form.descricao || !form.valor) return;
    try {
      await api.post("/financeiro/lancamentos", { ...form, valor: Number(form.valor) });
      toast("Lançamento registrado", "success");
      setForm({ tipo: "entrada", valor: 0, descricao: "" });
      load();
    } catch { toast("Erro ao criar", "error"); }
  };

  return (
    <div data-testid="financeiro-page">
      <div className="cta-inline">
        <div>
          <span className="content-eyebrow">Espaço de gestão</span>
          <h1 className="page-title">Financeiro</h1>
          <p className="page-sub">Um panorama simples do que entra e o que sai do seu espaço.</p>
        </div>
      </div>

      <div className="finance-hero" data-testid="finance-hero">
        <span className="lbl">Saldo do período</span>
        <span className="val">R$ {resumo.saldo.toFixed(2)}</span>
        <span className="sub">{resumo.lancamentos.length} lançamento(s) registrados</span>
        <div className="fin-summary">
          <div><span className="k">Entradas</span><span className="v">R$ {resumo.entradas.toFixed(2)}</span></div>
          <div><span className="k">Saídas</span><span className="v">R$ {resumo.saidas.toFixed(2)}</span></div>
          <div><span className="k">Saldo</span><span className="v">R$ {resumo.saldo.toFixed(2)}</span></div>
        </div>
      </div>

      <div className="grid-2" style={{ marginTop: 20 }}>
        <section className="card" data-testid="card-lancamentos">
          <span className="card-eyebrow">Últimos movimentos</span>
          <h3>Lançamentos</h3>
          <p className="desc">Histórico de entradas e saídas.</p>
          {resumo.lancamentos.length === 0 && <div className="empty"><h4>Sem movimentos</h4><p>Comece adicionando o primeiro lançamento.</p></div>}
          {resumo.lancamentos.map((l) => (
            <div key={l.id} className="list-item" data-testid={`lanc-${l.id}`}>
              <div className={`avatar-sm ${l.tipo === "entrada" ? "green" : ""}`}>
                {l.tipo === "entrada" ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
              </div>
              <div className="body">
                <strong>{l.descricao}</strong>
                <span className="sub">{new Date(l.data).toLocaleString("pt-BR")}</span>
              </div>
              <span className={`badge ${l.tipo === "entrada" ? "green" : "red"}`}>
                {l.tipo === "entrada" ? "+" : "-"} R$ {l.valor.toFixed(2)}
              </span>
            </div>
          ))}
        </section>

        <section className="card" data-testid="card-form-lanc">
          <span className="card-eyebrow">Novo lançamento</span>
          <h3>Registrar movimento</h3>
          <p className="desc">Adicione entradas de atendimentos ou saídas de compras.</p>
          <form onSubmit={submit}>
            <label className="field">Tipo
              <select value={form.tipo} onChange={(e) => setForm({ ...form, tipo: e.target.value })} data-testid="form-lanc-tipo">
                <option value="entrada">Entrada</option>
                <option value="saida">Saída</option>
              </select>
            </label>
            <label className="field">Descrição
              <input value={form.descricao} onChange={(e) => setForm({ ...form, descricao: e.target.value })} data-testid="form-lanc-desc" required />
            </label>
            <label className="field">Valor
              <input type="number" step="0.01" min="0" value={form.valor} onChange={(e) => setForm({ ...form, valor: e.target.value })} data-testid="form-lanc-valor" required />
            </label>
            <button type="submit" className="btn btn-primary" data-testid="btn-add-lanc"><Plus size={16} /> Registrar</button>
          </form>
        </section>
      </div>
    </div>
  );
}
