import { useEffect, useRef, useState } from "react";
import { Phone, Send, MessageCircle, Sparkles, RotateCcw, ArrowUp } from "lucide-react";
import { api, streamSSE } from "@/lib/api";
import { useToast } from "@/context/ToastContext";

const SESSION_KEY = "elo_chat_session";
const WELCOME = { role: "assistant", content: "Olá! Sou o Assistente ELO. Posso ajudar com a agenda de hoje, mensagens para clientes, estoque ou finanças. O que você precisa?" };

const DEMO_CONVERSAS = [
  { id: "c1", nome: "Amanda Martins", initials: "AM", ultima: "Posso agendar para sexta?", hora: "10:42", ativa: true },
  { id: "c2", nome: "João Costa", initials: "JC", ultima: "Obrigado pelo atendimento!", hora: "Ontem", green: true },
];

export default function Atendimento() {
  const toast = useToast();
  const [numero, setNumero] = useState("");
  const [clienteNome, setClienteNome] = useState("");
  const [mensagem, setMensagem] = useState("Olá! Passando para lembrar do seu atendimento na ELO Beauty Care. Confirma pra mim? 💕");
  const [gerando, setGerando] = useState(false);
  const [lembretes, setLembretes] = useState([]);

  const [sessionId, setSessionId] = useState(() => localStorage.getItem(SESSION_KEY) || "");
  const [msgs, setMsgs] = useState([WELCOME]);
  const [reply, setReply] = useState("");
  const [streaming, setStreaming] = useState(false);
  const endRef = useRef(null);

  useEffect(() => { api.get("/lembretes/").then(({ data }) => setLembretes(data)).catch(() => {}); }, []);

  useEffect(() => {
    const inicial = localStorage.getItem(SESSION_KEY);
    if (!inicial) return;
    api.get(`/ai/chat/${inicial}/messages`)
      .then(({ data }) => { if (data.length) setMsgs(data.map((m) => ({ role: m.role, content: m.content }))); })
      .catch(() => {});
  }, []);

  useEffect(() => { endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" }); }, [msgs]);

  const abrirWhats = () => {
    if (!numero.replace(/\D/g, "")) { toast("Informe o número do cliente", "error"); return; }
    window.open(`https://wa.me/${numero.replace(/\D/g, "")}?text=${encodeURIComponent(mensagem)}`, "_blank", "noopener,noreferrer");
    toast("Abrindo WhatsApp...", "success");
  };

  const registrar = async () => {
    if (!mensagem.trim()) { toast("Mensagem vazia", "error"); return; }
    try {
      const { data } = await api.post("/lembretes/", { mensagem, canal: numero ? `whatsapp:${numero}` : "whatsapp" });
      setLembretes((v) => [data, ...v]);
      toast("Lembrete registrado", "success");
    } catch { toast("Erro ao registrar lembrete", "error"); }
  };

  const gerarMensagem = async () => {
    setGerando(true);
    setMensagem("");
    try {
      await streamSSE("/ai/gerar-mensagem", { cliente_nome: clienteNome || null }, { onDelta: (d) => setMensagem((v) => v + d) });
      toast("Mensagem gerada pela IA", "success");
    } catch (ex) { toast(ex.message, "error"); }
    finally { setGerando(false); }
  };

  const enviar = async (e) => {
    e?.preventDefault();
    const texto = reply.trim();
    if (!texto || streaming) return;
    setReply("");
    setStreaming(true);
    setMsgs((v) => [...v, { role: "user", content: texto }, { role: "assistant", content: "", typing: true }]);
    try {
      await streamSSE("/ai/chat", { session_id: sessionId || null, message: texto }, {
        onMeta: (ev) => { if (ev.session_id && ev.session_id !== sessionId) { localStorage.setItem(SESSION_KEY, ev.session_id); setSessionId(ev.session_id); } },
        onDelta: (d) => setMsgs((v) => { const c = [...v]; const last = { ...c[c.length - 1] }; last.content += d; c[c.length - 1] = last; return c; }),
      });
    } catch (ex) {
      toast(ex.message, "error");
      setMsgs((v) => v.filter((m) => !(m.typing && !m.content)));
    } finally {
      setMsgs((v) => v.map((m) => ({ ...m, typing: false })));
      setStreaming(false);
    }
  };

  const novaConversa = () => {
    localStorage.removeItem(SESSION_KEY);
    setSessionId("");
    setMsgs([WELCOME]);
  };

  return (
    <div data-testid="atendimento-page">
      <div className="cta-inline">
        <div>
          <span className="content-eyebrow">Relacionamento</span>
          <h1 className="page-title">Atendimento inteligente</h1>
          <p className="page-sub">Central para acompanhar conversas, gerar mensagens com IA e abrir o WhatsApp em um clique.</p>
        </div>
        <div className="actions">
          <a className="btn-inline btn-wa" data-testid="btn-open-wa-top" href={`https://wa.me/${numero.replace(/\D/g, "") || ""}`} target="_blank" rel="noreferrer">
            <MessageCircle size={16} /> Abrir WhatsApp
          </a>
        </div>
      </div>

      <div className="grid-3">
        <section className="card" data-testid="card-transicao-direta">
          <span className="card-eyebrow">Transição direta</span>
          <h3>Envie um lembrete pelo WhatsApp</h3>
          <p className="desc">Digite o número do cliente e a mensagem — ou deixe a IA escrever para você.</p>

          <div className="grid-2" style={{ gap: 10 }}>
            <label className="field">
              Número (DDI + DDD)
              <input placeholder="55 42 99999-0000" value={numero} onChange={(e) => setNumero(e.target.value)} data-testid="input-numero-cliente" />
            </label>
            <label className="field">
              Nome da cliente
              <input placeholder="Ex: Amanda" value={clienteNome} onChange={(e) => setClienteNome(e.target.value)} data-testid="input-cliente-nome" />
            </label>
          </div>
          <label className="field">
            <span className="field-row">
              Mensagem
              <button type="button" className="btn-ai" onClick={gerarMensagem} disabled={gerando} data-testid="btn-gerar-mensagem-ia">
                <Sparkles size={13} /> {gerando ? "Escrevendo…" : "Gerar com IA"}
              </button>
            </span>
            <textarea rows={3} value={mensagem} onChange={(e) => setMensagem(e.target.value)} data-testid="input-mensagem" />
          </label>

          <div className="grid-2" style={{ gap: 10, marginTop: 8 }}>
            <button className="btn btn-primary" data-testid="btn-abrir-whatsapp" onClick={abrirWhats}>
              <Phone size={16} /> Abrir WhatsApp
            </button>
            <button className="btn btn-outline" data-testid="btn-registrar-lembrete" onClick={registrar}>
              <Send size={16} /> Registrar lembrete
            </button>
          </div>
        </section>

        <section className="card" data-testid="card-conversas">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
            <h3 style={{ fontSize: 18 }}>Conversas recentes</h3>
            <span className="badge rose">1 nova</span>
          </div>
          {DEMO_CONVERSAS.map((c) => (
            <div key={c.id} className={`list-item ${c.ativa ? "active" : ""}`} data-testid={`conversa-${c.id}`}>
              <div className={`avatar-sm ${c.green ? "green" : ""}`}>{c.initials}</div>
              <div className="body">
                <strong>{c.nome}</strong>
                <span className="sub">{c.ultima}</span>
              </div>
              <small className="meta">{c.hora}</small>
            </div>
          ))}
          {lembretes.length > 0 && (
            <div style={{ marginTop: 16, padding: "12px 0 0", borderTop: "1px solid var(--line)" }}>
              <span className="card-eyebrow">Lembretes registrados</span>
              {lembretes.slice(0, 3).map((l) => (
                <div key={l.id} className="list-item" data-testid={`lembrete-${l.id}`}>
                  <div className="avatar-sm">•</div>
                  <div className="body">
                    <strong style={{ fontSize: 13 }}>{l.mensagem.slice(0, 50)}{l.mensagem.length > 50 ? "…" : ""}</strong>
                    <span className="sub">{l.canal}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="card chat-card" data-testid="card-chat">
          <div className="chat-header">
            <div className="avatar-sm"><Sparkles size={16} /></div>
            <div className="body">
              <strong>Assistente ELO</strong>
              <small>Claude Sonnet 4.5 · conhece sua agenda, equipe e estoque</small>
            </div>
            <button type="button" className="topbar-icon" title="Nova conversa" onClick={novaConversa} data-testid="btn-nova-conversa">
              <RotateCcw size={15} />
            </button>
            <div className="chat-status" title="online" />
          </div>
          <div className="messages" data-testid="chat-messages">
            {msgs.map((m, i) => (
              <div key={i} className={`msg ${m.role === "user" ? "user" : "bot"} ${m.typing ? "typing" : ""}`} data-testid={`msg-${i}`}>{m.content}</div>
            ))}
            <div ref={endRef} />
          </div>
          <form className="chat-input" onSubmit={enviar}>
            <input placeholder="Pergunte sobre a agenda, clientes, estoque…" value={reply} onChange={(e) => setReply(e.target.value)} disabled={streaming} data-testid="input-reply" />
            <button type="submit" disabled={streaming || !reply.trim()} data-testid="btn-send-reply"><ArrowUp size={16} /></button>
          </form>
        </section>
      </div>
    </div>
  );
}
