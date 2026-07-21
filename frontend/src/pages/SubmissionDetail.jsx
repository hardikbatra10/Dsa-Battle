import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, Code2 } from 'lucide-react';
import { getSubmissionDetail } from '../api/submissions';
import { getApiErrorMessage } from '../api/axios';
import { LANGUAGE_LABELS, formatDateTime } from '../utils/formatters';
import { VerdictBadge } from '../components/common/Badge';
import CodeEditor from '../components/CodeEditor/CodeEditor';
import ErrorBanner from '../components/common/ErrorBanner';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';
import TestCaseResult from '../components/common/TestCaseResult';

export default function SubmissionDetail() {
  const { submissionId } = useParams();

  const [submission, setSubmission] = useState(null);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;

    async function load() {
      setIsLoading(true);
      setError('');
      try {
        const { data } = await getSubmissionDetail(submissionId);
        if (!cancelled) setSubmission(data);
      } catch (err) {
        if (!cancelled) {
          // The backend blocks viewing other participants' code mid-contest.
          setError(
            err.response?.status === 403
              ? "You can't view another participant's submission while the contest is still active."
              : getApiErrorMessage(err, 'Could not load this submission.')
          );
        }
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [submissionId]);

  if (isLoading) {
    return (
      <div className="flex justify-center py-16">
        <LoadingSpinner size={24} />
      </div>
    );
  }

  if (error || !submission) {
    return <ErrorBanner message={error || 'Submission not found.'} />;
  }

  return (
    <div className="mx-auto max-w-3xl">
      <Link
        to={`/rooms/${submission.room_code}/submissions`}
        className="mb-4 inline-flex items-center gap-1.5 text-sm text-ink-soft hover:text-ink"
      >
        <ArrowLeft size={15} />
        Back to submissions
      </Link>

      <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-soft text-primary">
            <Code2 size={20} />
          </span>
          <div>
            <h1 className="text-lg font-semibold text-ink">{submission.problem_title}</h1>
            <p className="text-sm text-ink-soft">
              #{submission.id} · {submission.username} ·{' '}
              {LANGUAGE_LABELS[submission.language] || submission.language} ·{' '}
              {formatDateTime(submission.submitted_at)}
            </p>
          </div>
        </div>
        <VerdictBadge verdict={submission.verdict} />
      </div>

      {submission.failure_detail && (
        <div className="mb-4">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink-faint">
            Failing Test Case
          </p>
          <TestCaseResult
            result={{ ...submission.failure_detail, passed: false, verdict: submission.verdict }}
          />
        </div>
      )}

      <div className="h-[520px] overflow-hidden rounded-xl border border-border">
        <CodeEditor language={submission.language} value={submission.code} readOnly />
      </div>
    </div>
  );
}
