import { Link } from 'react-router-dom';
import { Code2, ChevronRight } from 'lucide-react';
import { VerdictBadge, DifficultyBadge } from '../common/Badge';
import { LANGUAGE_LABELS, formatDateTime } from '../../utils/formatters';

export default function SubmissionCard({ submission }) {
  return (
    <Link
      to={`/submissions/${submission.id}`}
      className="flex items-center justify-between gap-4 rounded-xl border border-border bg-surface p-4 transition-colors hover:border-primary/40 hover:bg-surface-2"
    >
      <div className="flex min-w-0 items-center gap-3">
        <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-surface-2 text-ink-soft">
          <Code2 size={16} />
        </span>
        <div className="min-w-0">
          <p className="flex items-center gap-2 truncate text-sm font-medium text-ink">
            {submission.problem_title}
            {submission.difficulty && <DifficultyBadge difficulty={submission.difficulty} />}
          </p>
          <p className="mt-0.5 truncate text-xs text-ink-faint">
            {submission.username} · {LANGUAGE_LABELS[submission.language] || submission.language} ·{' '}
            {formatDateTime(submission.submitted_at)}
          </p>
        </div>
      </div>
      <div className="flex shrink-0 items-center gap-3">
        <VerdictBadge verdict={submission.verdict} />
        <ChevronRight size={16} className="text-ink-faint" />
      </div>
    </Link>
  );
}
