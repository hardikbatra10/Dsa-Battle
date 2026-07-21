import { Link, NavLink as RouterNavLink, useNavigate } from 'react-router-dom';
import { Swords, LogOut, User, Plus, LogIn } from 'lucide-react';
import { useAuth } from '../../hooks/useAuth';

function NavItem({ to, icon: Icon, children }) {
  return (
    <RouterNavLink
      to={to}
      className={({ isActive }) =>
        `inline-flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
          isActive ? 'bg-primary-soft text-primary' : 'text-ink-soft hover:bg-surface-2 hover:text-ink'
        }`
      }
    >
      {Icon && <Icon size={16} />}
      <span className="hidden sm:inline">{children}</span>
    </RouterNavLink>
  );
}

export default function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate('/login');
  }

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-bg/85 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6">
        <Link
          to={isAuthenticated ? '/dashboard' : '/'}
          className="flex items-center gap-2 font-semibold tracking-tight text-ink"
        >
          <Swords size={20} className="text-primary" />
          <span>Peer Code</span>
        </Link>

        {isAuthenticated ? (
          <nav className="flex items-center gap-1">
            <NavItem to="/dashboard">Dashboard</NavItem>
            <NavItem to="/rooms/create" icon={Plus}>
              Create Room
            </NavItem>
            <NavItem to="/rooms/join" icon={LogIn}>
              Join Room
            </NavItem>
            <NavItem to="/profile" icon={User}>
              {user?.username || 'Profile'}
            </NavItem>
            <button
              onClick={handleLogout}
              className="ml-1 inline-flex items-center gap-1.5 rounded-lg px-3 py-2 text-sm font-medium text-ink-soft transition-colors hover:bg-surface-2 hover:text-ink"
            >
              <LogOut size={16} />
              <span className="hidden sm:inline">Logout</span>
            </button>
          </nav>
        ) : (
          <nav className="flex items-center gap-2">
            <Link
              to="/login"
              className="rounded-lg px-3 py-2 text-sm font-medium text-ink-soft transition-colors hover:text-ink"
            >
              Log in
            </Link>
            <Link
              to="/register"
              className="rounded-lg bg-primary px-3.5 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-hover"
            >
              Sign up
            </Link>
          </nav>
        )}
      </div>
    </header>
  );
}
