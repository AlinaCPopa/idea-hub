import { useEffect, useState } from 'react';
import { api } from '../api/client';
import { useAuth } from '../hooks/useAuth';
import { User } from '../api/generated/types';

export default function UsersList() {
  const [users, setUsers] = useState<User[]>([]);
  const { token } = useAuth();

  useEffect(() => {
    if (!token) return;
    (async () => {
      const res = await api.get('/users');
      setUsers(res.data);
    })();
  }, [token]);

  if (!token) return <div className="text-sm">Login to view users.</div>;

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Users</h1>
      <ul className="list-disc pl-5 text-sm">
        {users.map(u => <li key={u.id}>{u.username}</li>)}
      </ul>
    </div>
  );
}
