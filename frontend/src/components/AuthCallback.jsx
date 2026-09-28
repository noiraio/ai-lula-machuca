import { useEffect, useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
import { useToast } from "@/context/ToastContext";

export default function AuthCallback() {
  const { processSession } = useAuth();
  const nav = useNavigate();
  const location = useLocation();
  const toast = useToast();
  const processed = useRef(false);

  useEffect(() => {
    if (processed.current) return;
    processed.current = true;
    const sessionId = new URLSearchParams(location.hash.replace(/^#/, "")).get("session_id");
    (async () => {
      try {
        await processSession(sessionId);
        window.history.replaceState(null, "", location.pathname);
        toast("Bem-vinda de volta", "success");
        nav("/app/atendimento", { replace: true });
      } catch {
        window.history.replaceState(null, "", "/");
        toast("Não foi possível entrar com o Google", "error");
        nav("/", { replace: true });
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return <div className="loading" data-testid="auth-callback">Conectando sua conta Google…</div>;
}
