import { useEffect, useRef } from 'react';

// Repeatedly calls `callback` every `intervalMs`, starting immediately.
// Used for lobby/leaderboard "live" updates until WebSockets exist.
// Pass `enabled = false` to pause polling (e.g. once a room is finished).
export function usePolling(callback, intervalMs, enabled = true) {
  const callbackRef = useRef(callback);
  callbackRef.current = callback;

  useEffect(() => {
    if (!enabled) return undefined;

    callbackRef.current();
    const id = setInterval(() => callbackRef.current(), intervalMs);
    return () => clearInterval(id);
  }, [intervalMs, enabled]);
}
