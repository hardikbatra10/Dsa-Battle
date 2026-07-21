import { DifficultyBadge, Badge } from '../common/Badge';
import { TOPIC_LABELS } from '../../utils/formatters';

// Full detail view of a single problem: title, badges, description and
// examples. Used inside the contest page's problem panel.
export default function ProblemCard({ problem }) {
  if (!problem) return null;

  return (
    <div className="flex flex-col gap-5">
      <div className="flex flex-wrap items-center gap-2">
        <h2 className="text-lg font-semibold text-ink">{problem.title}</h2>
        <DifficultyBadge difficulty={problem.difficulty} />
        <Badge>{TOPIC_LABELS[problem.topic] || problem.topic}</Badge>
      </div>

      <p className="whitespace-pre-wrap text-sm leading-relaxed text-ink-soft">{problem.description}</p>

      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <p className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-ink-faint">
            Example Input
          </p>
          <pre className="overflow-x-auto rounded-lg border border-border bg-surface-2 p-3 font-mono text-xs text-ink">
            {problem.example_input}
          </pre>
        </div>
        <div>
          <p className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-ink-faint">
            Example Output
          </p>
          <pre className="overflow-x-auto rounded-lg border border-border bg-surface-2 p-3 font-mono text-xs text-ink">
            {problem.example_output}
          </pre>
        </div>
      </div>

      {problem.constraints && (
        <div>
          <p className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-ink-faint">
            Constraints
          </p>
          <pre className="whitespace-pre-wrap rounded-lg border border-border bg-surface-2 p-3 font-mono text-xs text-ink-soft">
            {problem.constraints}
          </pre>
        </div>
      )}
    </div>
  );
}
