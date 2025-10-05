import { FormEvent, useState } from 'react';
import { api } from '../api/client';
import { useNavigate } from 'react-router-dom';

export default function IdeasCreate() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const navigate = useNavigate();

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    await api.post('/ideas', { title, description });
    navigate('/');
  }

  return (
    <form onSubmit={onSubmit} className="max-w-lg space-y-4">
      <h1 className="text-2xl font-semibold">Create Idea</h1>
      <label className="flex flex-col gap-1 text-sm">
        <span>Title</span>
        <input value={title} onChange={e => setTitle(e.target.value)} className="border rounded px-2 py-1" />
      </label>
      <label className="flex flex-col gap-1 text-sm">
        <span>Description</span>
        <textarea value={description} onChange={e => setDescription(e.target.value)} className="border rounded px-2 py-1" />
      </label>
      <button type="submit" className="bg-indigo-600 text-white px-4 py-2 rounded">Save</button>
    </form>
  );
}
