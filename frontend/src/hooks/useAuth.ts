import { createContext, createElement, ReactNode, useCallback, useContext, useMemo, useState } from 'react';
import { api } from '../api/client';

type AuthContextValue = {
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
};

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));

  const login = useCallback(async (username: string, password: string) => {
    const form = new URLSearchParams();
    form.set('username', username);
    form.set('password', password);
    const res = await api.post('/auth/login', form, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
    setToken(res.data.access_token);
    localStorage.setItem('token', res.data.access_token);
  }, [setToken]);

  const logout = useCallback(() => {
    setToken(null);
    localStorage.removeItem('token');
  }, [setToken]);

  const value = useMemo(() => ({ token, login, logout }), [token, login, logout]);

  return createElement(AuthContext.Provider, { value }, children);
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return ctx;
}
