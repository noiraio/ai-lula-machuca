import { NavLink, Outlet, useLocation, useNavigate } from "react-router-dom";
import { Calendar, User, MessageCircle, Package, DollarSign, Settings, Shield, HelpCircle, Search } from "lucide-react";
import { useAuth } from "@/context/AuthContext";

const NAV = [
  { to: "/app/agenda", label: "Agenda", icon: Calendar },
  { to: "/app/perfil", label: "Perfil", icon: User },
  { to: "/app/atendimento", label: "Atendimento", icon: MessageCircle },
  { to: "/app/estoque", label: "Estoque", icon: Package },
  { to: "/app/financeiro", label: "Financeiro", icon: DollarSign },
  { to: "/app/configuracoes", label: "Configurações", icon: Settings },
];

const CRUMBS = {
  "/app/agenda": ["Visão geral", "Agenda"],
  "/app/perfil": ["Visão geral", "Perfil"],
  "/app/atendimento": ["Visão geral", "Atendimento"],
  "/app/estoque": ["Visão geral", "Estoque"],
  "/app/financeiro": ["Visão geral", "Financeiro"],
  "/app/configuracoes": ["Visão geral", "Configurações"],
};

export default function AppShell() {
  const { user, logout } = useAuth();
  const loc = useLocation();
  const nav = useNavigate();
  const crumbs = CRUMBS[loc.pathname] || ["Visão geral", "Agenda"];
  const currentLabel = crumbs[1];
  const initials = (user?.nome || "AE").split(" ").map((n) => n[0]).slice(0, 2).join("").toUpperCase();

  const doLogout = async () => { await logout(); nav("/"); };

  return (
    <div className="app-shell">
      <aside className="sidebar" data-testid="app-sidebar">
        <div className="sidebar-brand">
          <span className="mono">E</span>
          <div>
            <strong>ELO</strong>
            <small>beauty care</small>
          </div>
        </div>

        <div>
          <span className="sidebar-eyebrow">Espaço de gestão</span>
          <nav className="sidebar-nav">
            {NAV.map((n) => (
              <NavLink key={n.to} to={n.to} data-testid={`nav-${n.label.toLowerCase()}`}
                className={({ isActive }) => `sidebar-item ${isActive ? "active" : ""}`}>
                <n.icon size={18} />
                <span>{n.label}</span>
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="sidebar-bottom">
          <button className="sidebar-item" data-testid="nav-account-security" onClick={doLogout}>
            <Shield size={18} />
            <span>Conta e segurança</span>
          </button>
        </div>
      </aside>

      <div className="main">
        <div className="topbar">
          <div className="topbar-crumbs">
            <span>{crumbs[0]}</span>
            <span className="sep">›</span>
            <span className="active">{crumbs[1]}</span>
          </div>
          <div className="topbar-search">
            <Search size={16} />
            <input placeholder={`Buscar em ${currentLabel}`} data-testid="topbar-search" />
            <span className="topbar-kbd">⌘K</span>
          </div>
          <button className="topbar-icon" data-testid="topbar-help" aria-label="Ajuda">
            <HelpCircle size={18} />
          </button>
          <div className="topbar-user">
            <div className="topbar-avatar" data-testid="topbar-avatar">{initials}</div>
            <div>
              <strong>{user?.nome || "Admin ELO"}</strong>
              <small>{user?.business || "ELO Beauty Care"}</small>
            </div>
          </div>
        </div>

        <div className="content">
          <Outlet />
        </div>
      </div>
    </div>
  );
}
