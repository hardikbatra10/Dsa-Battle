import { useState, useCallback } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { Copy, Check, Users, Crown, Clock, LogOut, Play } from 'lucide-react';
import { getRoom, startRoom, leaveRoom } from '../api/rooms';
import { getApiErrorMessage } from '../api/axios';
import { useAuth } from '../hooks/useAuth';
import { usePolling } from '../hooks/usePolling';
import { TOPIC_LABELS } from '../utils/formatters';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import ErrorBanner from '../components/common/ErrorBanner';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';
import { StatusBadge, DifficultyBadge, Badge } from '../components/common/Badge';

const POLL_INTERVAL_MS = 3000;

export default function RoomLobby() {
  const { roomCode } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [room, setRoom] = useState(null);
  const [loadError, setLoadError] = useState('');
  const [actionError, setActionError] = useState('');
  const [isStarting, setIsStarting] = useState(false);
  const [isLeaving, setIsLeaving] = useState(false);
  const [isCopied, setIsCopied] = useState(false);

  const fetchRoom = useCallback(async () => {
    try {
      const { data } = await getRoom(roomCode);
      setRoom(data);
      setLoadError('');

      // The moment the creator starts the room, every participant polling
      // this page picks up status === 'active' and jumps to the contest.
      if (data.status === 'active') {
        navigate(`/rooms/${roomCode}/contest`, { replace: true });
      }
    } catch (err) {
      setLoadError(getApiErrorMessage(err, 'Could not load this room.'));
    }
  }, [roomCode, navigate]);

  usePolling(fetchRoom, POLL_INTERVAL_MS, true);

  async function handleStart() {
    setActionError('');
    setIsStarting(true);
    try {
      await startRoom(roomCode);
      navigate(`/rooms/${roomCode}/contest`, { replace: true });
    } catch (err) {
      setActionError(getApiErrorMessage(err, 'Could not start the room.'));
      setIsStarting(false);
    }
  }

  async function handleLeave() {
    if (!window.confirm('Leave this room?')) return;
    setActionError('');
    setIsLeaving(true);
    try {
      await leaveRoom(roomCode);
      navigate('/dashboard');
    } catch (err) {
      setActionError(getApiErrorMessage(err, 'Could not leave the room.'));
      setIsLeaving(false);
    }
  }

  function handleCopy() {
    navigator.clipboard.writeText(roomCode);
    setIsCopied(true);
    setTimeout(() => setIsCopied(false), 1500);
  }

  if (loadError && !room) {
    return <ErrorBanner message={loadError} />;
  }

  if (!room) {
    return (
      <div className="flex justify-center py-24">
        <LoadingSpinner size={28} />
      </div>
    );
  }

  const isCreator = room.creator_username === user?.username;

  return (
    <div className="mx-auto max-w-2xl">
      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-ink-faint">Room</p>
          <div className="mt-1 flex items-center gap-2">
            <h1 className="font-mono text-2xl font-semibold text-ink">{room.room_code}</h1>
            <button
              onClick={handleCopy}
              className="flex items-center gap-1 rounded-md border border-border bg-surface-2 px-2 py-1 text-xs text-ink-soft transition-colors hover:text-ink"
            >
              {isCopied ? <Check size={13} className="text-success" /> : <Copy size={13} />}
              {isCopied ? 'Copied' : 'Copy'}
            </button>
          </div>
        </div>
        <StatusBadge status={room.status} />
      </div>

      {room.status === 'finished' && (
        <ErrorBanner message="This contest has already finished." className="mb-4" />
      )}

      <Card className="mb-4">
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-ink-faint">
          Battle Settings
        </h2>
        <dl className="grid grid-cols-2 gap-4 text-sm sm:grid-cols-4">
          <div>
            <dt className="text-ink-faint">Topic</dt>
            <dd className="mt-1">
              <Badge>{TOPIC_LABELS[room.topic] || room.topic}</Badge>
            </dd>
          </div>
          <div>
            <dt className="text-ink-faint">Difficulty</dt>
            <dd className="mt-1">
              <DifficultyBadge difficulty={room.difficulty} />
            </dd>
          </div>
          <div>
            <dt className="text-ink-faint">Problems</dt>
            <dd className="mt-1 text-ink">{room.number_of_questions}</dd>
          </div>
          <div>
            <dt className="text-ink-faint">Duration</dt>
            <dd className="mt-1 flex items-center gap-1 text-ink">
              <Clock size={13} />
              {room.time_limit_minutes}m
            </dd>
          </div>
        </dl>
      </Card>

      <Card className="mb-4">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase tracking-wide text-ink-faint">
            Participants ({room.participant_usernames.length})
          </h2>
          <Users size={16} className="text-ink-faint" />
        </div>
        <ul className="flex flex-col gap-2">
          {room.participant_usernames.map((username) => (
            <li
              key={username}
              className="flex items-center gap-2 rounded-lg bg-surface-2 px-3 py-2 text-sm text-ink"
            >
              {username === room.creator_username && <Crown size={14} className="text-warning" />}
              {username}
              {username === user?.username && <span className="ml-auto text-xs text-ink-faint">You</span>}
            </li>
          ))}
        </ul>
      </Card>

      <ErrorBanner message={actionError} className="mb-4" />

      <div className="flex flex-wrap gap-3">
        {isCreator && room.status === 'waiting' && (
          <Button onClick={handleStart} isLoading={isStarting} className="flex-1">
            <Play size={16} />
            Start Room
          </Button>
        )}
        {room.status !== 'active' && (
          <Button variant="secondary" onClick={handleLeave} isLoading={isLeaving}>
            <LogOut size={16} />
            Leave Room
          </Button>
        )}
        {room.status === 'finished' && (
          <Link to={`/rooms/${roomCode}/leaderboard`}>
            <Button variant="secondary">View Leaderboard</Button>
          </Link>
        )}
      </div>

      {!isCreator && room.status === 'waiting' && (
        <p className="mt-4 text-xs text-ink-faint">
          Waiting for the room creator to start the contest…
        </p>
      )}
    </div>
  );
}
