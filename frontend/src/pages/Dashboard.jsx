import { Link } from 'react-router-dom';
import { Plus, LogIn as JoinIcon, User } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import Card from '../components/common/Card';

export default function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="flex flex-col gap-8">
      <div>
        <h1 className="text-2xl font-semibold text-ink">Welcome back, {user?.username}</h1>
        <p className="mt-1 text-sm text-ink-soft">
          Create a room to challenge your friends, or join one with a code.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Link to="/rooms/create" className="group">
          <Card className="flex h-full flex-col gap-3 transition-colors group-hover:border-primary/50">
            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-soft text-primary">
              <Plus size={20} />
            </span>
            <div>
              <h2 className="text-base font-semibold text-ink">Create Room</h2>
              <p className="mt-1 text-sm text-ink-soft">
                Pick a topic, difficulty and time limit, then invite friends with a room code.
              </p>
            </div>
          </Card>
        </Link>

        <Link to="/rooms/join" className="group">
          <Card className="flex h-full flex-col gap-3 transition-colors group-hover:border-primary/50">
            <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-soft text-primary">
              <JoinIcon size={20} />
            </span>
            <div>
              <h2 className="text-base font-semibold text-ink">Join Room</h2>
              <p className="mt-1 text-sm text-ink-soft">
                Got a room code from a friend? Jump straight into the lobby.
              </p>
            </div>
          </Card>
        </Link>
      </div>

      <div>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-ink-faint">Your stats</h2>
        <div className="grid gap-4 sm:grid-cols-3">
          <StatCard label="Problems Solved" value={user?.problems_solved} />
          <StatCard label="Total Submissions" value={user?.total_submissions} />
          <StatCard label="Rooms Created" value={user?.rooms_created} />
        </div>
      </div>

      <Link
        to="/profile"
        className="inline-flex w-fit items-center gap-1.5 text-sm font-medium text-primary hover:underline"
      >
        <User size={15} />
        View full profile
      </Link>
    </div>
  );
}

function StatCard({ label, value }) {
  return (
    <Card>
      <p className="text-2xl font-semibold text-ink">{value ?? '—'}</p>
      <p className="mt-1 text-sm text-ink-soft">{label}</p>
    </Card>
  );
}
