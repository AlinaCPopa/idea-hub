import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export default function Navbar() {
  const { token, logout } = useAuth();
  return (
    <nav className="bg-indigo-600 text-white px-4 py-3 shadow">
      <div className="container mx-auto flex items-center gap-4">
        <Link to="/" className="font-bold tracking-wide">IdeaHub</Link>
        <Link to="/ideas/new">New Idea</Link>
        <Link to="/users">Users</Link>
        <div className="flex-1" />
        {token ? (
          <button onClick={logout} className="text-sm underline">Logout</button>
        ) : (
          <Link to="/login">Login</Link>
        )}
      </div>
    </nav>
  );
}
