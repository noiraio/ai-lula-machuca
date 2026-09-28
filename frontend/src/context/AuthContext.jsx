import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { api } from "@/lib/api";

const AuthCtx = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadMe = useCallback(async () => {
    const token = localStorage.getItem("elo_token");
    if (!token) { setUser(null); setLoading(false); return; }
    try {
      const { data } = await api.get("/auth/me");
      setUser(data);
    } catch {
      localStorage.removeItem("elo_token");
      setUser(null);
    } finally { setLoading(false); }
  }, []);

  useEffect(() => {
    // Ao voltar do Google, o AuthCallback troca o session_id antes de qualquer /me.
    if (window.location.hash?.includes("session_id=")) { setLoading(false); return; }
    loadMe();
  }, [loadMe]);

  const login = async (email, senha) => {
    const { data } = await api.post("/auth/login", { email, senha });
    localStorage.setItem("elo_token", data.access_token);
    await loadMe();
  };

  const register = async (payload) => {
    const { data } = await api.post("/auth/register", payload);
    localStorage.setItem("elo_token", data.access_token);
    await loadMe();
  };

  const loginWithGoogle = () => {
    // REMINDER: DO NOT HARDCODE THE URL, OR ADD ANY FALLBACKS OR REDIRECT URLS, THIS BREAKS THE AUTH
    const redirectUrl = window.location.origin + "/app/atendimento";
    window.location.href = `https://auth.emergentagent.com/?redirect=${encodeURIComponent(redirectUrl)}`;
  };

  const processSession = async (sessionId) => {
    const { data } = await api.post("/auth/session", { session_id: sessionId });
    localStorage.setItem("elo_token", data.access_token);
    setUser(data.user);
    setLoading(false);
    return data.user;
  };

  const logout = async () => {
    try { await api.post("/auth/logout"); } catch { /* sessão já inválida */ }
    localStorage.removeItem("elo_token");
    setUser(null);
  };

  const updateProfile = async (payload) => {
    const { data } = await api.put("/auth/me", payload);
    setUser(data);
    return data;
  };

  return (
    <AuthCtx.Provider value={{ user, loading, login, register, loginWithGoogle, processSession, logout, updateProfile }}>
      {children}
    </AuthCtx.Provider>
  );
}

export const useAuth = () => useContext(AuthCtx);
