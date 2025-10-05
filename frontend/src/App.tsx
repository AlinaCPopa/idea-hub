import { Route, Routes, Link } from 'react-router-dom';
import Home from './pages/Home';
import Login from './pages/Login';
import IdeasCreate from './pages/IdeasCreate';
import UsersList from './pages/UsersList';
import Navbar from './components/Navbar';

export default function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Navbar />
      <main className="flex-1 container mx-auto p-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/ideas/new" element={<IdeasCreate />} />
          <Route path="/users" element={<UsersList />} />
          <Route path="*" element={<div>Not Found <Link to="/">Home</Link></div>} />
        </Routes>
      </main>
    </div>
  );
}
