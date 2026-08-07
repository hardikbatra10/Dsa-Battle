import { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { User, Trophy, Send, Layers, Crown, CheckCircle2, History } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { getMyRooms } from '../api/rooms';
import { getMySubmissions } from '../api/submissions';
import { getApiErrorMessage } from '../api/axios';
import { TOPIC_LABELS, formatDateTime } from '../utils/formatters';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import ErrorBanner from '../components/common/ErrorBanner';
import EmptyState from '../components/common/EmptyState';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';
import SubmissionCard from '../components/SubmissionCard/SubmissionCard';
import { Badge, DifficultyBadge, StatusBadge } from '../components/common/Badge';

export default function Profile() {
  const { user, refreshUser } = useAuth();

  const [rooms, setRooms] = useState(null);
  const [submissions, setSubmissions] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    refreshUser();
  }, [refreshUser]);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setIsLoading(true);
      setError('');
      try {
        const [roomsRes, submissionsRes] = await Promise.all([getMyRooms(), getMySubmissions()]);
        if (cancelled) return;
        setRooms(roomsRes.data);
        setSubmissions(submissionsRes.data);
      } catch (err) {
        if (!cancelled) setError(getApiErrorMessage(err, 'Could not load your profile activity.'));
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, []);

  // One card per problem, keeping only the most recent accepted submission —
  // submissions arrive newest-first, so the first accepted hit per problem is it.
  const solvedProblems = useMemo(() => {
    if (!submissions) return [];
    const seen = new Set();
    const result = [];
    for (const submission of submissions) {
      if (submission.verdict !== 'accepted' || seen.has(submission.problem_title)) continue;
      seen.add(submission.problem_title);
      result.push(submission);
    }
    return result;
  }, [submissions]);

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

      <div className="mb-10 grid gap-4 sm:grid-cols-3">
        <StatCard icon={Trophy} label="Problems Solved" value={user.problems_solved} />
        <StatCard icon={Send} label="Total Submissions" value={user.total_submissions} />
        <StatCard icon={Layers} label="Rooms Created" value={user.rooms_created} />
      </div>

      {error && <ErrorBanner message={error} className="mb-6" />}

      {isLoading ? (
        <div className="flex justify-center py-16">
          <LoadingSpinner size={24} />
        </div>
      ) : (
        <div className="flex flex-col gap-10">
          <section>
            <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-ink-faint">
              <Layers size={14} />
              Your Rooms
            </h2>
            {rooms.length === 0 ? (
              <EmptyState
                icon={Layers}
                title="No rooms yet"
                description="Create or join a room to start battling."
                action={
                  <Link to="/dashboard">
                    <Button variant="secondary">Go to Dashboard</Button>
                  </Link>
                }
              />
            ) : (
              <div className="flex flex-col gap-3">
                {rooms.map((room) => (
                  <RoomRow key={room.room_code} room={room} />
                ))}
              </div>
            )}
          </section>

          <section>
            <h2 className="mb-3 flex items-center gap-2 text-sm font-semibold uppercase tracking-wide text-ink-faint">
              <CheckCircle2 size={14} />
              Solved Problems
            </h2>
            {solvedProblems.length === 0 ? (
              <EmptyState
                icon={History}
                title="No problems solved yet"
                description="Accepted solutions will show up here, with a link back to your code."
              />
            ) : (
              <div className="flex flex-col gap-3">
                {solvedProblems.map((submission) => (
                  <SubmissionCard key={submission.id} submission={submission} />
                ))}
              </div>
            )}
          </section>
        </div>
      )}
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

function RoomRow({ room }) {
  return (
    <Card className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex min-w-0 flex-col gap-2">
        <div className="flex flex-wrap items-center gap-2">
          <span className="font-mono text-sm font-semibold text-ink">{room.room_code}</span>
          {room.is_creator && <Crown size={14} className="text-warning" />}
          <StatusBadge status={room.status} />
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <Badge>{TOPIC_LABELS[room.topic] || room.topic}</Badge>
          <DifficultyBadge difficulty={room.difficulty} />
          <span className="text-xs text-ink-faint">{formatDateTime(room.created_at)}</span>
        </div>
      </div>

      <div className="flex shrink-0 items-center gap-2">
        {room.status === 'waiting' ? (
          <Link to={`/rooms/${room.room_code}`}>
            <Button variant="secondary" className="text-xs">
              Open Room
            </Button>
          </Link>
        ) : (
          <>
            <Link to={`/rooms/${room.room_code}/leaderboard`}>
              <Button variant="secondary" className="text-xs">
                <Trophy size={13} />
                Leaderboard
              </Button>
            </Link>
            <Link to={`/rooms/${room.room_code}/submissions`}>
              <Button variant="ghost" className="text-xs">
                <Send size={13} />
                Submissions
              </Button>
            </Link>
          </>
        )}
      </div>
    </Card>
  );
}
