import { Check } from 'lucide-react';

const LETTERS = 'ABCDEFGHIJ';

// Left-hand problem navigation for the contest page: A/B/C... list with a
// checkmark once the current user has an accepted submission for that problem.
export default function ProblemSidebar({ problems, activeProblemId, solvedProblemIds, onSelect }) {
  return (
    <nav className="flex flex-col gap-1 p-3">
      {problems.map((problem, index) => {
        const isActive = problem.id === activeProblemId;
        const isSolved = solvedProblemIds.has(problem.id);

        return (
          <button
            key={problem.id}
            type="button"
            onClick={() => onSelect(problem.id)}
            className={`flex items-center gap-2.5 rounded-lg px-3 py-2.5 text-left text-sm transition-colors ${
              isActive ? 'bg-primary-soft text-primary' : 'text-ink-soft hover:bg-surface-2 hover:text-ink'
            }`}
          >
            <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-md border border-border bg-surface-2 text-xs font-semibold text-ink-soft">
              {LETTERS[index] || index + 1}
            </span>
            <span className="flex-1 truncate">{problem.title}</span>
            {isSolved && <Check size={15} className="shrink-0 text-success" />}
          </button>
        );
      })}
    </nav>
  );
}
