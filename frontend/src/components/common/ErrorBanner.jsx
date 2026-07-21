import { AlertTriangle } from 'lucide-react';

export default function ErrorBanner({ message, className = '' }) {
  if (!message) return null;

  return (
    <div
      className={`flex items-start gap-2 rounded-lg border border-error/30 bg-error-soft px-3.5 py-2.5 text-sm text-error ${className}`}
    >
      <AlertTriangle size={16} className="mt-0.5 shrink-0" />
      <span>{message}</span>
    </div>
  );
}
