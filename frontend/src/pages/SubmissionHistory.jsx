import { useState, useCallback, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { History, ArrowLeft } from 'lucide-react';
import { getSubmissionHistory } from '../api/submissions';
import { getApiErrorMessage } from '../api/axios';
import SubmissionCard from '../components/SubmissionCard/SubmissionCard';
import EmptyState from '../components/common/EmptyState';
import ErrorBanner from '../components/common/ErrorBanner';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';

export default function SubmissionHistory() {
  const { roomCode } = useParams();
  const [filter, setFilter] = useState('all'); // 'all' | 'mine'
  const [submissions, setSubmissions] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  const load = useCallback(async () => {
    setIsLoading(true);
    setError('');
    try {
      const { data } = await getSubmissionHistory(roomCode, { mine: filter === 'mine' });
      setSubmissions(data);
    } catch (err) {
      setError(getApiErrorMessage(err, 'Could not load submission history.'));
    } finally {
      setIsLoading(false);
    }
  }, [roomCode, filter]);

  useEffect(() => {
    load();
  }, [load]);

  return (
    <div className="mx-auto max-w-2xl">
      <Link
        to={`/rooms/${roomCode}`}
        className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-ink"
      >
        <ArrowLeft size={15} />
        Back to room
      </Link>

      <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-soft text-primary">
            <History size={20} />
          </span>
          <div>
            <h1 className="text-xl font-semibold text-ink">Submission History</h1>
            <p className="font-mono text-sm text-ink-soft">{roomCode}</p>
          </div>
        </div>

        <div className="flex rounded-lg border border-border bg-surface-2 p-1">
          <FilterButton active={filter === 'all'} onClick={() => setFilter('all')}>
            All Submissions
          </FilterButton>
          <FilterButton active={filter === 'mine'} onClick={() => setFilter('mine')}>
            My Submissions
          </FilterButton>
        </div>
      </div>

      {error && <ErrorBanner message={error} className="mb-4" />}

      {isLoading ? (
        <div className="flex justify-center py-16">
          <LoadingSpinner size={24} />
        </div>
      ) : submissions && submissions.length === 0 ? (
        <EmptyState
          icon={History}
          title="No submissions yet"
          description={
            filter === 'mine'
              ? "You haven't submitted anything in this room yet."
              : 'No one has submitted a solution yet.'
          }
        />
      ) : (
        <div className="flex flex-col gap-3">
          {submissions?.map((submission) => (
            <SubmissionCard key={submission.id} submission={submission} />
          ))}
        </div>
      )}
    </div>
  );
}

function FilterButton({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
        active ? 'bg-primary text-white' : 'text-ink-soft hover:text-ink'
      }`}
    >
      {children}
    </button>
  );
}
