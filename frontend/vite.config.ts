import { defineConfig, loadEnv } from 'vite';
// Minimal process typing to avoid needing @types/node in this template
// eslint-disable-next-line @typescript-eslint/no-explicit-any
declare const process: any;
import react from '@vitejs/plugin-react';

// Export a function form so we can read mode-specific env vars for dynamic host whitelisting
export default ({ mode }: { mode: string }) => {
  const env = loadEnv(mode, process.cwd(), ''); // load all (no prefix filter)

  const allowed = new Set<string>(['localhost', '127.0.0.1']);

  if (env.VITE_ALLOWED_HOSTS) {
    env.VITE_ALLOWED_HOSTS.split(',')
      .map(h => h.trim())
      .filter(Boolean)
      .forEach(h => allowed.add(h));
  }

  // Single deploy host convenience variable (optional)
  if (env.VITE_DEPLOY_HOST) {
    allowed.add(env.VITE_DEPLOY_HOST.trim());
  }

  return defineConfig({
    plugins: [react()],
    server: {
      port: 5173,
      allowedHosts: Array.from(allowed),
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: path => path.replace(/^\/api/, '')
        }
      }
    }
  });
};
