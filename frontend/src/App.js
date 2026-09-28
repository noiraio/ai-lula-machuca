import { BrowserRouter, Navigate, Route, Routes, useLocation } from "react-router-dom";
import "@/App.css";
import { AuthProvider, useAuth } from "@/context/AuthContext";
import { ToastProvider } from "@/context/ToastContext";
import Landing from "@/pages/Landing";
import AppShell from "@/components/AppShell";
import AuthCallback from "@/components/AuthCallback";
import Agenda from "@/pages/Agenda";
import Perfil from "@/pages/Perfil";
import Atendimento from "@/pages/Atendimento";
import Estoque from "@/pages/Estoque";
import Financeiro from "@/pages/Financeiro";
import Configuracoes from "@/pages/Configuracoes";

function Protected({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading">Carregando…</div>;
  if (!user) return <Navigate to="/" replace />;
  return children;
}

function PublicOnly({ children }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="loading">Carregando…</div>;
  if (user) return <Navigate to="/app/atendimento" replace />;
  return children;
}

function AppRouter() {
  const location = useLocation();
  if (location.hash?.includes("session_id=")) return <AuthCallback />;
  return (
    <Routes>
      <Route path="/" element={<PublicOnly><Landing /></PublicOnly>} />
      <Route path="/app" element={<Protected><AppShell /></Protected>}>
        <Route index element={<Navigate to="/app/atendimento" replace />} />
        <Route path="agenda" element={<Agenda />} />
        <Route path="perfil" element={<Perfil />} />
        <Route path="atendimento" element={<Atendimento />} />
        <Route path="estoque" element={<Estoque />} />
        <Route path="financeiro" element={<Financeiro />} />
        <Route path="configuracoes" element={<Configuracoes />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <ToastProvider>
      <AuthProvider>
        <BrowserRouter>
          <AppRouter />
        </BrowserRouter>
      </AuthProvider>
    </ToastProvider>
  );
}
