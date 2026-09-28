import { useEffect, useState } from "react";
import { Sparkles, Send, MessageCircle, CheckCircle2, AlertTriangle, RefreshCw } from "lucide-react";
import { api, streamSSE } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

const hora = (iso) => new Date(iso).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
const waLink = (item) => `https://wa.me/${(item.telefone_e164 || "").replace("+", "")}?text=${encodeURIComponent(item.lembrete?.mensagem || "")}`;
const initials = (n) => (n || "C").split(" ").map((p) => p[0]).slice(0, 2).join("").toUpperCase();

function LinhaLembrete({ item, config, onChange }) {
  const toast = useToast();
  const [texto, setTexto] = useState(item.lembrete?.mensagem || "");
  const [enviando, setEnviando] = useState(false);
  useEffect(() => { setTexto(item.lembrete?.mensagem || ""); }, [item.lembrete?.mensagem]);

  const enviado = !!item.lembrete?.enviado_em;

  const salvar = async () => {
    const t = texto.trim();
    if (!t || t === item.lembrete?.mensagem) return;
    try { const { data } = await api.put(`/lembretes/vespera/${item.id}`, { mensagem: t }); onChange(data); }
    catch { toast("Erro ao salvar mensagem", "error"); }
  };

  const enviar = async (canal) => {
    if (!texto.trim()) { toast("Gere ou escreva a mensagem primeiro", "error"); return; }
    setEnviando(true);
    try {
      const { data } = await api.post(`/lembretes/vespera/${item.id}/enviar`, { canal, mensagem: texto.trim() });
      if (data.item) onChange(data.item);
      if (data.ok) toast(canal === "twilio" ? `Enviado para ${item.cliente_nome || "cliente"}` : "Marcado como enviado", "success");
      else toast(data.detalhe || "Falha no envio", "error");
    } catch (ex) { toast(ex.response?.data?.detail || "Falha no envio", "error"); }
    finally { setEnviando(false); }
  };

  return (
    <div className={`vespera-row ${enviado ? "sent" : ""}`} data-testid={`vespera-${item.id}`}>
      <div className="vespera-who">
        <div className={`avatar-sm ${enviado ? "green" : ""}`}>{initials(item.cliente_nome)}</div>
        <div className="body">
          <strong>{item.cliente_nome || "Cliente"}</strong>
          <span className="sub">{hora(item.data_hora_inicio)} · {item.servico_nome} · com {item.profissional_nome}</span>
          <span className="sub mono-tel">{item.telefone_e164 || item.cliente_telefone || "sem telefone"}</span>
        </div>
        {enviado ? (
          <span className="badge green" data-testid={`vespera-status-${item.id}`}><CheckCircle2 size={11} /> enviado {hora(item.lembrete.enviado_em)}</span>
        ) : item.lembrete?.erro ? (
          <span className="badge red" title={item.lembrete.erro} data-testid={`vespera-status-${item.id}`}><AlertTriangle size={11} /> falhou</span>
        ) : texto ? (
          <span className="badge gold" data-testid={`vespera-status-${item.id}`}>pronta</span>
        ) : (
          <span className="badge rose" data-testid={`vespera-status-${item.id}`}>pendente</span>
        )}
      </div>
      <textarea
        className="vespera-text"
        rows={2}
        placeholder="Clique em “Gerar todas com IA” ou escreva a mensagem aqui…"
        value={texto}
        onChange={(e) => setTexto(e.target.value)}
        onBlur={salvar}
        data-testid={`vespera-msg-${item.id}`}
      />
      <div className="vespera-actions">
        <a
          className={`btn-inline btn-wa small ${!texto || !item.telefone_e164 ? "disabled" : ""}`}
          href={texto && item.telefone_e164 ? waLink({ ...item, lembrete: { mensagem: texto } }) : undefined}
          target="_blank" rel="noreferrer"
          onClick={(e) => { if (!texto || !item.telefone_e164) { e.preventDefault(); return; } if (!enviado) enviar("whatsapp_link"); }}
          data-testid={`vespera-wa-${item.id}`}
        >
          <MessageCircle size={14} /> WhatsApp
        </a>
        <button
          type="button"
          className="btn-inline small primary"
          disabled={!config.twilio_configurado || enviando || enviado || !texto}
          title={config.twilio_configurado ? "Enviar automaticamente via Twilio" : "Configure o Twilio para envio automático"}
          onClick={() => enviar("twilio")}
          data-testid={`vespera-send-${item.id}`}
        >
          <Send size={14} /> {enviando ? "Enviando…" : "Enviar"}
        </button>
      </div>
    </div>
  );
}

export default function LembretesVespera() {
  const toast = useToast();
  const [itens, setItens] = useState([]);
  const [config, setConfig] = useState({ twilio_configurado: false, sandbox: false });
  const [gerando, setGerando] = useState(false);
  const [enviandoTodos, setEnviandoTodos] = useState(false);
  const [carregado, setCarregado] = useState(false);

  const load = async () => {
    try {
      const [{ data: lista }, { data: cfg }] = await Promise.all([api.get("/lembretes/vespera"), api.get("/lembretes/config")]);
      setItens(lista); setConfig(cfg);
    } catch { toast("Erro ao carregar lembretes de amanhã", "error"); }
    finally { setCarregado(true); }
  };
  useEffect(() => { load(); /* eslint-disable-next-line */ }, []);

  const patch = (novo) => setItens((v) => v.map((i) => (i.id === novo.id ? novo : i)));

  const gerarTodas = async () => {
    if (!itens.length) return;
    setGerando(true);
    let falhas = 0;
    try {
      await streamSSE("/ai/lembretes-vespera", {}, {
        onMeta: (ev) => {
          if (ev.agendamento_id) {
            setItens((v) => v.map((i) => i.id === ev.agendamento_id
              ? { ...i, lembrete: { ...(i.lembrete || {}), mensagem: ev.mensagem, gerado_em: new Date().toISOString() } }
              : i));
          }
          if (ev.falha) falhas += 1;
        },
      });
      toast(falhas ? `Geradas com ${falhas} falha(s)` : "Mensagens geradas pela IA", falhas ? "warning" : "success");
    } catch (ex) { toast(ex.message, "error"); }
    finally { setGerando(false); }
  };

  const enviarTodas = async () => {
    setEnviandoTodos(true);
    try {
      const { data } = await api.post("/lembretes/vespera/enviar-todos");
      data.forEach((r) => r.item && patch(r.item));
      const ok = data.filter((r) => r.ok).length;
      toast(`${ok}/${data.length} lembrete(s) enviados`, ok === data.length ? "success" : "warning");
    } catch (ex) { toast(ex.response?.data?.detail || "Falha no envio em lote", "error"); }
    finally { setEnviandoTodos(false); }
  };

  const pendentesComTexto = itens.filter((i) => i.lembrete?.mensagem && !i.lembrete?.enviado_em).length;
  const enviados = itens.filter((i) => i.lembrete?.enviado_em).length;

  return (
    <section className="card vespera-card" data-testid="card-lembretes-vespera">
      <div className="vespera-head">
        <div>
          <span className="card-eyebrow">Confirmação automática</span>
          <h3>Lembretes de amanhã</h3>
          <p className="desc">
            {carregado && itens.length === 0
              ? "Nenhum agendamento para amanhã."
              : `${itens.length} atendimento(s) amanhã · ${enviados} enviado(s). A IA escreve uma mensagem personalizada para cada cliente.`}
          </p>
        </div>
        <div className="vespera-cta">
          <button type="button" className="topbar-icon" title="Atualizar" onClick={load} data-testid="btn-vespera-refresh"><RefreshCw size={15} /></button>
          <button type="button" className="btn-ai lg" onClick={gerarTodas} disabled={gerando || !itens.length} data-testid="btn-gerar-todas-ia">
            <Sparkles size={14} /> {gerando ? "Escrevendo…" : "Gerar todas com IA"}
          </button>
          <button
            type="button"
            className="btn-inline primary"
            onClick={enviarTodas}
            disabled={!config.twilio_configurado || enviandoTodos || pendentesComTexto === 0}
            title={config.twilio_configurado ? "Envia via Twilio todas as mensagens prontas" : "Configure o Twilio para enviar em lote"}
            data-testid="btn-enviar-todas"
          >
            <Send size={14} /> {enviandoTodos ? "Enviando…" : `Enviar todas${pendentesComTexto ? ` (${pendentesComTexto})` : ""}`}
          </button>
        </div>
      </div>

      {!config.twilio_configurado && carregado && (
        <div className="vespera-note" data-testid="twilio-off-note">
          <AlertTriangle size={14} />
          <span>
            Envio automático desativado. Preencha <code>TWILIO_ACCOUNT_SID</code>, <code>TWILIO_AUTH_TOKEN</code> e <code>TWILIO_WHATSAPP_FROM</code> no <code>backend/.env</code> (veja <code>INTEGRACAO_WHATSAPP.md</code>). Enquanto isso, use o botão WhatsApp de cada cliente.
          </span>
        </div>
      )}
      {config.twilio_configurado && config.sandbox && (
        <div className="vespera-note" data-testid="twilio-sandbox-note">
          <AlertTriangle size={14} />
          <span>Twilio em modo <strong>Sandbox</strong>: só recebe quem enviou “join &lt;código&gt;” para {config.remetente}.</span>
        </div>
      )}

      <div className="vespera-list">
        {itens.map((item) => <LinhaLembrete key={item.id} item={item} config={config} onChange={patch} />)}
      </div>
    </section>
  );
}
