import { useState } from 'react';
import { Navigate, useNavigate } from 'react-router-dom';
import { setUsername as setUsernameRequest } from '../api/auth';
import { getApiErrorMessage } from '../api/axios';
import { useAuth } from '../hooks/useAuth';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import ErrorBanner from '../components/common/ErrorBanner';
import Card from '../components/common/Card';
import PeerCodeLogo from '../components/common/PeerCodeLogo';

const MIN = 3;
const MAX = 20;
const ALLOWED = /^[A-Za-z0-9_]*$/;

/**
 * One-time username setup for accounts created through Google.
 *
 * Those accounts start with a placeholder derived from the email address,
 * which is not something anyone wants on a leaderboard. The backend decides
 * whether this step is owed (`needs_username` on the profile); this page only
 * renders it.
 */
export default function ChooseUsername() {
  const { user, refreshUser } = useAuth();
  const navigate = useNavigate();

  const [value, setValue] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Nothing to do here if the name is already chosen - arriving by typing the
  // URL should not present a form that can only fail.
  if (user && !user.needs_username) {
    return <Navigate to="/dashboard" replace />;
  }

  // Mirrors the server's rules so the common mistakes are caught before a
  // round trip. The server still enforces them; this is only for speed.
  const localError =
    value && !ALLOWED.test(value)
      ? 'Use only letters, numbers and underscores.'
      : value && value.length < MIN
        ? `At least ${MIN} characters.`
        : '';

  async function handleSubmit(event) {
    event.preventDefault();
    if (localError) return;

    setError('');
    setIsSubmitting(true);
    try {
      await setUsernameRequest(value.trim());
      // Re-read the profile so needs_username flips and the guard stops
      // redirecting back here.
      await refreshUser();
      navigate('/dashboard', { replace: true });
    } catch (err) {
      setError(getApiErrorMessage(err, 'Could not set that username.'));
      setIsSubmitting(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-sm flex-col items-center py-10">
      <div className="mb-8 flex items-center gap-2 text-lg font-semibold text-ink">
        <PeerCodeLogo className="text-primary" size={22} />
        Peer Code
      </div>

      <Card className="w-full">
        <h1 className="mb-1 text-xl font-semibold text-ink">Pick a username</h1>
        <p className="mb-6 text-sm text-ink-soft">
          This is the name other players see on leaderboards. You can&apos;t change it
          later, so choose one you like.
        </p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Input
            id="username"
            label="Username"
            autoComplete="off"
            autoFocus
            value={value}
            maxLength={MAX}
            onChange={(e) => setValue(e.target.value)}
            required
          />
          <p className="-mt-2 text-xs text-ink-faint">
            {MIN}–{MAX} characters. Letters, numbers and underscores.
          </p>

          <ErrorBanner message={localError || error} />

          <Button
            type="submit"
            isLoading={isSubmitting}
            disabled={!value || !!localError}
            className="w-full"
          >
            Continue
          </Button>
        </form>
      </Card>
    </div>
  );
}
