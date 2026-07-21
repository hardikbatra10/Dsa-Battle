import { Link } from 'react-router-dom';
import { Swords } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

// Compact, full-height chrome for the contest page: logo | room code | timer | user.
// Deliberately skips the normal Navbar/Footer so the code editor gets maximum
// vertical space.
export default function ContestLayout({ roomCode, timerSlot, children }) {
  const { user } = useAuth();

  return (
    <div className="flex h-svh flex-col bg-bg">
      <header className="flex h-14 shrink-0 items-center justify-between border-b border-border bg-surface px-4 sm:px-6">
        <div className="flex items-center gap-3">
          <Link to="/dashboard" className="flex items-center gap-2 font-semibold text-ink">
            <Swords size={18} className="text-primary" />
            <span className="hidden sm:inline">DSA Battle</span>
          </Link>
          {roomCode && (
            <span className="rounded-md border border-border bg-surface-2 px-2 py-1 font-mono text-xs text-ink-soft">
              {roomCode}
            </span>
          )}
        </div>
        <div className="flex items-center gap-4">
          {timerSlot}
          <span className="hidden text-sm text-ink-soft sm:inline">{user?.username}</span>
        </div>
      </header>
      <div className="min-h-0 flex-1">{children}</div>
    </div>
  );
}
