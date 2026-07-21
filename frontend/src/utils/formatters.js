// Label/color maps mirror the exact choice values defined on the Django models.
// Keep these in sync with backend/problems/models.py, backend/rooms/models.py,
// and backend/submissions/models.py if those choices ever change.

export const DIFFICULTY_LABELS = {
  easy: 'Easy',
  medium: 'Medium',
  hard: 'Hard',
};

export const TOPIC_LABELS = {
  array: 'Array',
  trees: 'Trees',
  graphs: 'Graphs',
  dp: 'DP',
};

export const ROOM_STATUS_LABELS = {
  waiting: 'Waiting',
  active: 'Active',
  finished: 'Finished',
};

export const VERDICT_LABELS = {
  accepted: 'Accepted',
  pending: 'Pending',
  wrong_answer: 'Wrong Answer',
  runtime_error: 'Runtime Error',
  compilation_error: 'Compilation Error',
  time_limit_exceeded: 'Time Limit Exceeded',
};

// The Submission model's LANGUAGE_CHOICES also includes "javascript", but the
// Judge0 service (submissions/services/judge0.py) has no mapping for it and
// would crash with a 500. It is intentionally left out of the UI.
export const LANGUAGE_LABELS = {
  cpp: 'C++',
  java: 'Java',
  python: 'Python',
};

export function formatDateTime(isoString) {
  if (!isoString) return '—';
  const date = new Date(isoString);
  return date.toLocaleString(undefined, {
    dateStyle: 'medium',
    timeStyle: 'short',
  });
}

export function formatCountdown(totalSeconds) {
  const clamped = Math.max(0, Math.floor(totalSeconds));
  const minutes = Math.floor(clamped / 60);
  const seconds = clamped % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}
