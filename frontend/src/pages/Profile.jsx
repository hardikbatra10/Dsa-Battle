import { useEffect } from 'react';
import { User, Trophy, Send, Layers } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import Card from '../components/common/Card';

export default function Profile() {
  const { user, refreshUser } = useAuth();

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  if (!user) return null;

  return (
    <div className="mx-auto max-w-2xl">
      <div className="mb-8 flex items-center gap-4">
        <span className="flex h-14 w-14 items-center justify-center rounded-full bg-primary-soft text-primary">
          <User size={26} />
        </span>
        <div>
          <h1 className="text-xl font-semibold text-ink">{user.username}</h1>
          <p className="text-sm text-ink-soft">{user.email}</p>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <StatCard icon={Trophy} label="Problems Solved" value={user.problems_solved} />
        <StatCard icon={Send} label="Total Submissions" value={user.total_submissions} />
        <StatCard icon={Layers} label="Rooms Created" value={user.rooms_created} />
      </div>
    </div>
  );
}

function StatCard({ icon: Icon, label, value }) {
  return (
    <Card className="flex flex-col gap-3">
      <span className="flex h-9 w-9 items-center justify-center rounded-lg bg-surface-2 text-ink-soft">
        <Icon size={17} />
      </span>
      <div>
        <p className="text-2xl font-semibold text-ink">{value ?? '—'}</p>
        <p className="mt-0.5 text-sm text-ink-soft">{label}</p>
      </div>
    </Card>
  );
}
