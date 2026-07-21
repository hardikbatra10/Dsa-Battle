import { Link } from 'react-router-dom';
import { Compass } from 'lucide-react';
import Button from '../components/common/Button';

export default function NotFound() {
  return (
    <div className="mx-auto flex max-w-md flex-col items-center gap-4 py-24 text-center">
      <Compass size={32} className="text-ink-faint" />
      <div>
        <h1 className="text-xl font-semibold text-ink">Page not found</h1>
        <p className="mt-1 text-sm text-ink-soft">The page you're looking for doesn't exist.</p>
      </div>
      <Link to="/dashboard">
        <Button variant="secondary">Back to Dashboard</Button>
      </Link>
    </div>
  );
}
