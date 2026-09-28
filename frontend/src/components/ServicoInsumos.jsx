import { useEffect, useState } from "react";
import { ChevronDown, ChevronUp, Plus, Trash2, Package } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

export default function ServicoInsumos({ servico, insumos }) {
  const toast = useToast();
  const [open, setOpen] = useState(false);
  const [rels, setRels] = useState(null);
  const [form, setForm] = useState({ insumo_id: "", quantidade_utilizada: 1 });

  const load = async () => {
    try { const { data } = await api.get(`/servicos/${servico.id}/insumos`); setRels(data); }
    catch { toast("Erro ao carregar insumos do serviço", "error"); }
  };
  useEffect(() => { if (open && rels === null) load(); /* eslint-disable-next-line */ }, [open]);

  const add = async (e) => {
    e.preventDefault();
    if (!form.insumo_id) { toast("Escolha um insumo", "error"); return; }
    try {
      const { data } = await api.post(`/servicos/${servico.id}/insumos`, { insumo_id: form.insumo_id, quantidade_utilizada: Number(form.quantidade_utilizada) });
      setRels(data);
      setForm({ insumo_id: "", quantidade_utilizada: 1 });
      toast("Insumo vinculado", "success");
    } catch (ex) { toast(ex.response?.data?.detail || "Erro ao vincular", "error"); }
  };

  const remove = async (insumoId) => {
    try { await api.delete(`/servicos/${servico.id}/insumos/${insumoId}`); setRels((v) => v.filter((r) => r.insumo_id !== insumoId)); toast("Vínculo removido", "success"); }
    catch { toast("Erro ao remover", "error"); }
  };

  const disponiveis = insumos.filter((i) => !(rels || []).some((r) => r.insumo_id === i.id));
  const count = rels?.length;

  return (
    <div className="si-wrap">
      <button type="button" className="si-toggle" onClick={() => setOpen((v) => !v)} data-testid={`btn-toggle-insumos-${servico.id}`}>
        <Package size={13} /> Insumos consumidos{typeof count === "number" ? ` (${count})` : ""}
        {open ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
      </button>
      {open && (
        <div className="si-panel" data-testid={`servico-insumos-${servico.id}`}>
          {rels === null && <p className="si-empty">Carregando…</p>}
          {rels?.length === 0 && <p className="si-empty">Nenhum insumo vinculado. Ao concluir um atendimento deste serviço, nada será descontado do estoque.</p>}
          {rels?.map((r) => (
            <div key={r.id} className="si-row" data-testid={`si-${servico.id}-${r.insumo_id}`}>
              <span className="si-name">{r.insumo_nome}</span>
              <span className={`badge ${r.quantidade_atual <= r.quantidade_minima_alerta ? "red" : "green"}`}>{r.quantidade_atual} un em estoque</span>
              <span className="si-qty">−{r.quantidade_utilizada} / atendimento</span>
              <button type="button" className="topbar-icon" onClick={() => remove(r.insumo_id)} data-testid={`btn-del-si-${servico.id}-${r.insumo_id}`} title="Remover vínculo"><Trash2 size={13} /></button>
            </div>
          ))}
          <form className="si-form" onSubmit={add}>
            <select value={form.insumo_id} onChange={(e) => setForm({ ...form, insumo_id: e.target.value })} data-testid={`form-si-insumo-${servico.id}`}>
              <option value="">Escolher insumo…</option>
              {disponiveis.map((i) => <option key={i.id} value={i.id}>{i.nome} ({i.quantidade_atual} un)</option>)}
            </select>
            <input type="number" min="0.1" step="0.1" value={form.quantidade_utilizada} onChange={(e) => setForm({ ...form, quantidade_utilizada: e.target.value })} data-testid={`form-si-qtd-${servico.id}`} title="Quantidade por atendimento" />
            <button type="submit" className="btn-inline small primary" data-testid={`btn-add-si-${servico.id}`}><Plus size={13} /> Vincular</button>
          </form>
        </div>
      )}
    </div>
  );
}
