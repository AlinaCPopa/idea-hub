import { useEffect, useState } from 'react';
import { IdeaCard } from '../components/IdeaCard';
import { Idea } from '../api/generated/types';
import { useAuth } from '../hooks/useAuth';
import { api } from '../api/client';
import { Link } from 'react-router-dom';

export default function Home() {
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const { token } = useAuth();

  async function load() {
    const res = await api.get('/ideas');
    setIdeas(res.data);
  }
  useEffect(() => { load(); }, []);

  async function like(id: number) {
    await api.post(`/ideas/${id}/like`);
    await load();
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-4">
        <h1 className="text-2xl font-semibold">Ideas</h1>
        <Link to="/ideas/new" className="text-sm underline">Create</Link>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {ideas.map(i => (
          <div key={i.id} className="relative group">
            <IdeaCard idea={i} />
            {token && (
              <button onClick={() => like(i.id)} className="absolute top-2 right-2 bg-indigo-600 text-white text-xs px-2 py-1 rounded opacity-80 group-hover:opacity-100">Like</button>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
