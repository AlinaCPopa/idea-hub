import { FormEvent, useState } from 'react';
import { useAuth } from '../hooks/useAuth';

export function AuthForm() {
  const { login } = useAuth();
  const [username, setUsername] = useState('demo');
  const [password, setPassword] = useState('demo');
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    try {
      await login(username, password);
    } catch (err: any) {
      setError(err.message || 'Failed');
    }
  }

  return (
    <form onSubmit={onSubmit} className="max-w-sm mx-auto flex flex-col gap-4 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-semibold">Login</h2>
      {error && <div className="text-red-600 text-sm">{error}</div>}
      <label className="flex flex-col gap-1 text-sm">
        <span>Username</span>
        <input value={username} onChange={e => setUsername(e.target.value)} className="border rounded px-2 py-1" />
      </label>
      <label className="flex flex-col gap-1 text-sm">
        <span>Password</span>
        <input type="password" value={password} onChange={e => setPassword(e.target.value)} className="border rounded px-2 py-1" />
      </label>
      <button type="submit" className="bg-indigo-600 text-white py-2 rounded hover:bg-indigo-500">Login</button>
    </form>
  );
}
