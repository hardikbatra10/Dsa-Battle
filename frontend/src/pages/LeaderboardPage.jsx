import { useState, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Trophy, ArrowLeft } from 'lucide-react';
import { getLeaderboard } from '../api/rooms';
import { getApiErrorMessage } from '../api/axios';
import { usePolling } from '../hooks/usePolling';
import { useAuth } from '../hooks/useAuth';
import Leaderboard from '../components/Leaderboard/Leaderboard';
import ErrorBanner from '../components/common/ErrorBanner';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';

const POLL_INTERVAL_MS = 5000;

export default function LeaderboardPage() {
  const { roomCode } = useParams();
  const { user } = useAuth();

  const [entries, setEntries] = useState(null);
  const [error, setError] = useState('');

  const fetchLeaderboard = useCallback(async () => {
    try {
      const { data } = await getLeaderboard(roomCode);
      setEntries(data);
      setError('');
    } catch (err) {
      setError(getApiErrorMessage(err, 'Could not load the leaderboard.'));
    }
  }, [roomCode]);

  usePolling(fetchLeaderboard, POLL_INTERVAL_MS, true);

  return (
    <div className="mx-auto max-w-2xl">
      <Link
        to={`/rooms/${roomCode}`}
        className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-ink"
      >
        <ArrowLeft size={15} />
        Back to room
      </Link>

      <div className="mb-6 flex items-center gap-3">
        <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-soft text-primary">
          <Trophy size={20} />
        </span>
        <div>
          <h1 className="text-xl font-semibold text-ink">Leaderboard</h1>
          <p className="font-mono text-sm text-ink-soft">{roomCode}</p>
        </div>
      </div>

      {error && !entries && <ErrorBanner message={error} />}

      {!entries ? (
        <div className="flex justify-center py-16">
          <LoadingSpinner size={24} />
        </div>
      ) : (
        <Leaderboard entries={entries} currentUsername={user?.username} />
      )}
    </div>
  );
}
