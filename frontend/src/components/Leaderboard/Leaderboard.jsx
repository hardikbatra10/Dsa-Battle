import { Trophy, Users } from 'lucide-react';
import EmptyState from '../common/EmptyState';

const RANK_COLOR = {
  1: 'text-warning',
  2: 'text-ink-soft',
  3: 'text-orange-400',
};

export default function Leaderboard({ entries = [], currentUsername }) {
  if (entries.length === 0) {
    return (
      <EmptyState
        icon={Users}
        title="No participants yet"
        description="The leaderboard fills in as participants join and submit solutions."
      />
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-border">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-border bg-surface-2 text-left text-xs uppercase tracking-wide text-ink-faint">
            <th className="px-4 py-3 font-medium">Rank</th>
            <th className="px-4 py-3 font-medium">Username</th>
            <th className="px-4 py-3 font-medium text-right">Solved</th>
            <th className="px-4 py-3 font-medium text-right">Attempts</th>
          </tr>
        </thead>
        <tbody>
          {entries.map((entry) => {
            const isMe = entry.username === currentUsername;
            return (
              <tr
                key={entry.username}
                className={`border-b border-border last:border-0 ${isMe ? 'bg-primary-soft' : ''}`}
              >
                <td className="px-4 py-3">
                  <span
                    className={`inline-flex items-center gap-1 font-semibold ${RANK_COLOR[entry.rank] || 'text-ink-faint'}`}
                  >
                    {entry.rank <= 3 && <Trophy size={14} />}#{entry.rank}
                  </span>
                </td>
                <td className="px-4 py-3 text-ink">
                  {entry.username}
                  {isMe && (
                    <span className="ml-2 rounded-full bg-primary-soft px-2 py-0.5 text-xs text-primary">
                      You
                    </span>
                  )}
                </td>
                <td className="px-4 py-3 text-right text-ink">{entry.solved}</td>
                <td className="px-4 py-3 text-right text-ink-soft">{entry.attempts}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
