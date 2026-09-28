import { createContext, useCallback, useContext, useState } from "react";

const Ctx = createContext(null);

export function ToastProvider({ children }) {
  const [items, setItems] = useState([]);
  const push = useCallback((message, variant = "default") => {
    const id = Math.random().toString(36).slice(2);
    setItems((v) => [...v, { id, message, variant }]);
    setTimeout(() => setItems((v) => v.filter((t) => t.id !== id)), 3000);
  }, []);
  return (
    <Ctx.Provider value={push}>
      {children}
      <div className="toasts" data-testid="toast-root">
        {items.map((t) => (
          <div key={t.id} className={`toast ${t.variant}`} data-testid={`toast-${t.variant}`}>{t.message}</div>
        ))}
      </div>
    </Ctx.Provider>
  );
}

export const useToast = () => useContext(Ctx);
