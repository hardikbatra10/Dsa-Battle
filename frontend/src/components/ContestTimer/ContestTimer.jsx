import { useEffect, useRef, useState } from 'react';
import { Clock } from 'lucide-react';
import { formatCountdown } from '../../utils/formatters';

function secondsRemaining(contestEndMs) {
  return Math.max(0, (contestEndMs - Date.now()) / 1000);
}

// Computes "time left" purely on the client from started_at + time_limit_minutes,
// so we never poll the server just to tick a clock. The backend independently
// re-validates the deadline on every submission, so this is a display-only timer.
export default function ContestTimer({ startedAt, timeLimitMinutes, onExpire, className = '' }) {
  const contestEndMs = new Date(startedAt).getTime() + timeLimitMinutes * 60 * 1000;
  const [remaining, setRemaining] = useState(() => secondsRemaining(contestEndMs));
  const hasFiredExpiry = useRef(false);

  useEffect(() => {
    hasFiredExpiry.current = false;
    const id = setInterval(() => {
      const value = secondsRemaining(contestEndMs);
      setRemaining(value);
      if (value <= 0 && !hasFiredExpiry.current) {
        hasFiredExpiry.current = true;
        onExpire?.();
      }
    }, 1000);
    return () => clearInterval(id);
  }, [contestEndMs, onExpire]);

  const isEnded = remaining <= 0;
  const isLow = remaining > 0 && remaining <= 5 * 60;

  const toneClass = isEnded
    ? 'border-error/30 bg-error-soft text-error'
    : isLow
      ? 'border-warning/30 bg-warning-soft text-warning'
      : 'border-border bg-surface-2 text-ink';

  return (
    <div className={`flex items-center gap-1.5 rounded-md border px-2.5 py-1 font-mono text-sm ${toneClass} ${className}`}>
      <Clock size={14} />
      {isEnded ? 'Ended' : formatCountdown(remaining)}
    </div>
  );
}
