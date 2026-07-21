import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Swords } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';
import { getApiErrorMessage } from '../api/axios';
import Input from '../components/common/Input';
import Button from '../components/common/Button';
import ErrorBanner from '../components/common/ErrorBanner';
import Card from '../components/common/Card';

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({ username: '', email: '', password: '', confirmPassword: '' });
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  function updateField(field) {
    return (event) => setForm((prev) => ({ ...prev, [field]: event.target.value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');

    if (form.password !== form.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    if (form.password.length < 6) {
      setError('Password must be at least 6 characters.');
      return;
    }

    setIsSubmitting(true);
    try {
      await register({ username: form.username, email: form.email, password: form.password });
      navigate('/login', { state: { registered: true } });
    } catch (err) {
      setError(getApiErrorMessage(err, 'Could not create your account.'));
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
        <h1 className="mb-1 text-xl font-semibold text-ink">Create your account</h1>
        <p className="mb-6 text-sm text-ink-soft">Register to start battling.</p>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          <Input
            id="username"
            label="Username"
            autoComplete="username"
            value={form.username}
            onChange={updateField('username')}
            required
          />
          <Input
            id="email"
            label="Email"
            type="email"
            autoComplete="email"
            value={form.email}
            onChange={updateField('email')}
            required
          />
          <Input
            id="password"
            label="Password"
            type="password"
            autoComplete="new-password"
            value={form.password}
            onChange={updateField('password')}
            required
            minLength={6}
          />
          <Input
            id="confirmPassword"
            label="Confirm Password"
            type="password"
            autoComplete="new-password"
            value={form.confirmPassword}
            onChange={updateField('confirmPassword')}
            required
            minLength={6}
          />
          <ErrorBanner message={error} />
          <Button type="submit" isLoading={isSubmitting} className="w-full">
            Sign up
          </Button>
        </form>
      </Card>

      <p className="mt-6 text-sm text-ink-soft">
        Already have an account?{' '}
        <Link to="/login" className="font-medium text-primary hover:underline">
          Log in
        </Link>
      </p>
    </div>
  );
}
