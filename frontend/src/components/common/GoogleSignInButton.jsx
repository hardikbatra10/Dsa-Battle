import { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { getApiErrorMessage } from '../../api/axios';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';
import ErrorBanner from './ErrorBanner';

/**
 * Google sign-in, shared by the login and register pages so the two cannot
 * drift apart.
 *
 * Renders nothing when Firebase is unconfigured, rather than a button that
 * fails on click.
 */
export default function GoogleSignInButton({ label = 'Continue with Google' }) {
  const { loginWithGoogle, isChatConfigured: isFirebaseReady } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [error, setError] = useState('');
  const [isBusy, setIsBusy] = useState(false);

  if (!isFirebaseReady) return null;

  async function handleClick() {
    setError('');
    setIsBusy(true);
    try {
      await loginWithGoogle();
      navigate(location.state?.from || '/dashboard', { replace: true });
    } catch (err) {
      // Closing the popup is a deliberate act, not an error worth shouting
      // about, so it leaves the form exactly as it was.
      const code = err?.code;
      if (
        code === 'auth/popup-closed-by-user' ||
        code === 'auth/cancelled-popup-request'
      ) {
        return;
      }
      if (code === 'auth/popup-blocked') {
        setError('Your browser blocked the sign-in popup. Allow popups and try again.');
        return;
      }
      setError(getApiErrorMessage(err, 'Google sign-in failed.'));
    } finally {
      setIsBusy(false);
    }
  }

  return (
    <div className="mt-5">
      <div className="mb-4 flex items-center gap-3">
        <span className="h-px flex-1 bg-border" />
        <span className="text-xs uppercase tracking-wide text-ink-faint">or</span>
        <span className="h-px flex-1 bg-border" />
      </div>

      <ErrorBanner message={error} className="mb-3" />

      <button
        type="button"
        onClick={handleClick}
        disabled={isBusy}
        className="inline-flex w-full items-center justify-center gap-2.5 rounded-lg border border-border bg-surface px-4 py-2.5 text-sm font-medium text-ink transition-colors hover:bg-surface-2 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {isBusy ? <LoadingSpinner size={16} /> : <GoogleMark />}
        {label}
      </button>
    </div>
  );
}

/** Google's four-colour mark. Inline so it needs no network request. */
function GoogleMark() {
  return (
    <svg width="16" height="16" viewBox="0 0 18 18" aria-hidden="true">
      <path
        fill="#4285F4"
        d="M17.64 9.2c0-.64-.06-1.25-.16-1.84H9v3.48h4.84a4.14 4.14 0 0 1-1.8 2.72v2.26h2.91c1.7-1.57 2.69-3.88 2.69-6.62Z"
      />
      <path
        fill="#34A853"
        d="M9 18c2.43 0 4.47-.8 5.96-2.18l-2.91-2.26c-.81.54-1.84.86-3.05.86-2.34 0-4.32-1.58-5.03-3.71H.96v2.34A8.99 8.99 0 0 0 9 18Z"
      />
      <path
        fill="#FBBC05"
        d="M3.97 10.71a5.41 5.41 0 0 1 0-3.42V4.96H.96a8.99 8.99 0 0 0 0 8.08l3.01-2.33Z"
      />
      <path
        fill="#EA4335"
        d="M9 3.58c1.32 0 2.5.45 3.44 1.35l2.58-2.59C13.46.89 11.43 0 9 0A8.99 8.99 0 0 0 .96 4.96l3.01 2.33C4.68 5.16 6.66 3.58 9 3.58Z"
      />
    </svg>
  );
}
