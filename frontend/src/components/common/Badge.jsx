import {
  DIFFICULTY_LABELS,
  VERDICT_LABELS,
  ROOM_STATUS_LABELS,
} from '../../utils/formatters';

const TONE_CLASSES = {
  neutral: 'bg-surface-2 text-ink-soft border-border',
  primary: 'bg-primary-soft text-primary border-primary/30',
  success: 'bg-success-soft text-success border-success/30',
  warning: 'bg-warning-soft text-warning border-warning/30',
  error: 'bg-error-soft text-error border-error/30',
};

export function Badge({ children, tone = 'neutral', className = '' }) {
  return (
    <span
      className={`inline-flex items-center gap-1 whitespace-nowrap rounded-full border px-2.5 py-1 text-xs font-medium ${TONE_CLASSES[tone]} ${className}`}
    >
      {children}
    </span>
  );
}

const DIFFICULTY_TONE = { easy: 'success', medium: 'warning', hard: 'error' };

export function DifficultyBadge({ difficulty }) {
  return (
    <Badge tone={DIFFICULTY_TONE[difficulty] || 'neutral'}>
      {DIFFICULTY_LABELS[difficulty] || difficulty}
    </Badge>
  );
}

const VERDICT_TONE = {
  accepted: 'success',
  pending: 'neutral',
  wrong_answer: 'error',
  runtime_error: 'error',
  compilation_error: 'error',
  time_limit_exceeded: 'warning',
};

export function VerdictBadge({ verdict }) {
  return (
    <Badge tone={VERDICT_TONE[verdict] || 'neutral'}>
      {VERDICT_LABELS[verdict] || verdict}
    </Badge>
  );
}

const STATUS_TONE = { waiting: 'warning', active: 'success', finished: 'neutral' };

export function StatusBadge({ status }) {
  return (
    <Badge tone={STATUS_TONE[status] || 'neutral'}>
      {ROOM_STATUS_LABELS[status] || status}
    </Badge>
  );
}
