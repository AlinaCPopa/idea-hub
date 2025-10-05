import axios from 'axios';

// In production we may set VITE_API_BASE (e.g. https://idea-hub.azurewebsites.net)
// Fallback to relative '/api' which can be reverse-proxied when deploying behind a single domain.
const baseURL = import.meta.env.VITE_API_BASE ? `${import.meta.env.VITE_API_BASE}` : '/api';

export const api = axios.create({
  baseURL,
});

api.interceptors.request.use(cfg => {
  const token = localStorage.getItem('token');
  if (token) {
    cfg.headers = cfg.headers || {};
    cfg.headers['Authorization'] = `Bearer ${token}`;
  }
  return cfg;
});
