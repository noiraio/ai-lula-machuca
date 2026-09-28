import { useEffect, useMemo, useState } from "react";
import { Plus, Check, Trash2 } from "lucide-react";
import { api } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

function fmtDay(d) {
  return { dow: d.toLocaleDateString("pt-BR", { weekday: "short" }).slice(0, 3).toUpperCase(), num: d.getDate() };
}

export default function Agenda() {
  const toast = useToast();
  const today = useMemo(() => new Date(new Date().setHours(0,0,0,0)), []);
  const [selected, setSelected] = useState(today);
  const [agendamentos, setAgendamentos] = useState([]);
  const [servicos, setServicos] = useState([]);
  const [profs, setProfs] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [form, setForm] = useState({ cliente_nome: "", cliente_telefone: "", servico_id: "", profissional_id: "", hora: "10:00" });

  const days = useMemo(() => {
    const arr = [];
    for (let i = -1; i < 6; i++) {
      const d = new Date(today); d.setDate(today.getDate() + i); arr.push(d);
    }
    return arr;
  }, [today]);

  const loadAll = async () => {
    const start = new Date(selected); start.setHours(0,0,0,0);
    const end = new Date(start); end.setDate(end.getDate() + 1);
    try {
      const [{ data: ags }, { data: srv }, { data: pro }] = await Promise.all([
        api.get("/agendamentos/", { params: { data_inicio: start.toISOString(), data_fim: end.toISOString() } }),
        api.get("/servicos/"),
        api.get("/profissionais/"),
      ]);
      setAgendamentos(ags);
      setServicos(srv);
      setProfs(pro);
    } catch { toast("Erro ao carregar agenda", "error"); }
  };

  useEffect(() => { loadAll(); /* eslint-disable-next-line */ }, [selected]);

  const criar = async (e) => {
    e.preventDefault();
    if (!form.servico_id || !form.profissional_id || !form.cliente_telefone) { toast("Preencha todos os campos", "error"); return; }
    const inicio = new Date(selected);
    const [h, m] = form.hora.split(":").map(Number);
    inicio.setHours(h, m, 0, 0);
    try {
      await api.post("/agendamentos/", {
        servico_id: form.servico_id,
        profissional_id: form.profissional_id,
        cliente_telefone: form.cliente_telefone,
        cliente_nome: form.cliente_nome || null,
        data_hora_inicio: inicio.toISOString(),
      });
      toast("Agendamento criado", "success");
      setShowForm(false);
      setForm({ cliente_nome: "", cliente_telefone: "", servico_id: "", profissional_id: "", hora: "10:00" });
      loadAll();
    } catch (ex) {
      toast(ex.response?.data?.detail || "Erro ao criar", "error");
    }
  };

  const concluir = async (id) => {
    try { await api.patch(`/agendamentos/${id}/concluir`); toast("Concluído", "success"); loadAll(); }
    catch (ex) { toast(ex.response?.data?.detail || "Erro", "error"); }
  };
  const remover = async (id) => {
    try { await api.delete(`/agendamentos/${id}`); toast("Excluído", "success"); loadAll(); }
    catch { toast("Erro", "error"); }
  };

  return (
    <div data-testid="agenda-page">
      <div className="cta-inline">
        <div>
          <span className="content-eyebrow">Espaço de gestão</span>
          <h1 className="page-title">Agenda</h1>
          <p className="page-sub">Acompanhe os atendimentos do dia com uma visão calma e organizada.</p>
        </div>
        <div className="actions">
          <button className="btn-inline" style={{ background: "var(--wine-2)", color: "#fff" }} onClick={() => setShowForm(true)} data-testid="btn-new-agendamento">
            <Plus size={16} /> Novo agendamento
          </button>
        </div>
      </div>

      <div className="day-strip" data-testid="day-strip">
        {days.map((d) => {
          const isSel = d.toDateString() === selected.toDateString();
          const isToday = d.toDateString() === today.toDateString();
          const { dow, num } = fmtDay(d);
          return (
            <button key={d.toISOString()} className={`day-chip ${isSel ? "selected" : ""} ${isToday ? "today" : ""}`} onClick={() => setSelected(d)} data-testid={`day-${num}`}>
              <span className="dow">{dow}</span>
              <span className="num">{num}</span>
            </button>
          );
        })}
      </div>

      <div className="grid-2">
        <section className="card" data-testid="card-hoje">
          <span className="card-eyebrow">{selected.toLocaleDateString("pt-BR", { weekday: "long", day: "2-digit", month: "long" })}</span>
          <h3>Agendamentos do dia</h3>
          <p className="desc">{agendamentos.length} atendimento(s) programado(s).</p>

          {agendamentos.length === 0 && (
            <div className="empty" data-testid="empty-agenda">
              <h4>Sem agendamentos</h4>
              <p>Nenhum compromisso registrado para esta data.</p>
            </div>
          )}
          {agendamentos.map((a, i) => {
            const inicio = new Date(a.data_hora_inicio);
            const color = a.status === "concluido" ? "green" : (i % 3 === 2 ? "gold" : "");
            return (
              <div key={a.id} className={`booking-item ${color}`} data-testid={`booking-${a.id}`}>
                <div className="booking-time">
                  <strong>{inicio.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" })}</strong>
                  <small>{a.servico_nome}</small>
                </div>
                <div className="booking-body">
                  <strong>{a.cliente_nome || "Cliente"}</strong>
                  <small>com {a.profissional_nome} • R$ {a.servico_valor.toFixed(2)}</small>
                </div>
                <span className={`badge ${a.status === "concluido" ? "green" : "rose"}`}>{a.status}</span>
                {a.status !== "concluido" && (
                  <button className="topbar-icon" onClick={() => concluir(a.id)} data-testid={`btn-concluir-${a.id}`} title="Concluir">
                    <Check size={16} />
                  </button>
                )}
                <button className="topbar-icon" onClick={() => remover(a.id)} data-testid={`btn-del-${a.id}`} title="Excluir">
                  <Trash2 size={16} />
                </button>
              </div>
            );
          })}
        </section>

        {showForm && (
          <section className="card" data-testid="card-form-agendamento">
            <span className="card-eyebrow">Novo compromisso</span>
            <h3>Registrar agendamento</h3>
            <p className="desc">Selecione o cliente, serviço e horário desejado.</p>
            <form onSubmit={criar}>
              <label className="field">Nome do cliente
                <input value={form.cliente_nome} onChange={(e) => setForm({ ...form, cliente_nome: e.target.value })} data-testid="form-cliente-nome" />
              </label>
              <label className="field">Telefone (DDI+DDD)
                <input value={form.cliente_telefone} onChange={(e) => setForm({ ...form, cliente_telefone: e.target.value })} placeholder="5511990000000" data-testid="form-cliente-tel" required />
              </label>
              <div className="grid-2">
                <label className="field">Serviço
                  <select value={form.servico_id} onChange={(e) => setForm({ ...form, servico_id: e.target.value })} data-testid="form-servico" required>
                    <option value="">Selecione</option>
                    {servicos.map((s) => <option key={s.id} value={s.id}>{s.nome} — R${s.valor.toFixed(2)}</option>)}
                  </select>
                </label>
                <label className="field">Profissional
                  <select value={form.profissional_id} onChange={(e) => setForm({ ...form, profissional_id: e.target.value })} data-testid="form-prof" required>
                    <option value="">Selecione</option>
                    {profs.map((p) => <option key={p.id} value={p.id}>{p.nome}</option>)}
                  </select>
                </label>
              </div>
              <label className="field">Horário
                <input type="time" value={form.hora} onChange={(e) => setForm({ ...form, hora: e.target.value })} data-testid="form-hora" required />
              </label>
              <div className="grid-2">
                <button type="submit" className="btn btn-primary" data-testid="form-submit">Confirmar</button>
                <button type="button" className="btn btn-outline" onClick={() => setShowForm(false)}>Cancelar</button>
              </div>
            </form>
          </section>
        )}
      </div>
    </div>
  );
}
