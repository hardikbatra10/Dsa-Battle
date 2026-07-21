import { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Swords } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { getApiErrorMessage } from '../api/axios';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import ErrorBanner from '../components/common/ErrorBanner';
import Card from '../components/common/Card';

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setIsSubmitting(true);

    try {
      await login({ username, password });
      const redirectTo = location.state?.from || '/dashboard';
      navigate(redirectTo, { replace: true });
    } catch (err) {
      setError(getApiErrorMessage(err, 'Invalid username or password.'));
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="mx-auto flex max-w-sm flex-col items-center py-10">
      <Link to="/" className="mb-8 flex items-center gap-2 text-lg font-semibold text-ink">
        <Swords className="text-primary" size={22} />
        DSA Battle
      </Link>

      <Card className="w-full">
        <h1 className="mb-1 text-xl font-semibold text-ink">Welcome back</h1>
        <p className="mb-6 text-sm text-ink-soft">Log in to join or create a battle room.</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Input
            id="username"
            label="Username"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
          <Input
            id="password"
            label="Password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          <ErrorBanner message={error} />
          <Button type="submit" isLoading={isSubmitting} className="w-full">
            Log in
          </Button>
        </form>
      </Card>

      <p className="mt-6 text-sm text-ink-soft">
        Don&apos;t have an account?{' '}
        <Link to="/register" className="font-medium text-primary hover:underline">
          Sign up
        </Link>
      </p>
    </div>
  );
}
