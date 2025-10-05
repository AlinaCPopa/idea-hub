import { useEffect, useState } from 'react';
import { api } from '../api/client';

type AuthContext = {
  token: string | null;
  login: (u: string, p: string) => Promise<void>;
  logout: () => void;
};

let singleton: AuthContext | null = null;

export function useAuth(): AuthContext {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'));

  async function login(username: string, password: string) {
    const form = new URLSearchParams();
    form.set('username', username);
    form.set('password', password);
    const res = await api.post('/auth/login', form, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
    setToken(res.data.access_token);
    localStorage.setItem('token', res.data.access_token);
  }
  function logout() {
    setToken(null);
    localStorage.removeItem('token');
  }

  // Keep a stable instance
  if (!singleton) {
    singleton = { token, login, logout } as AuthContext;
  } else {
    singleton.token = token;
  }
  return singleton;
}
