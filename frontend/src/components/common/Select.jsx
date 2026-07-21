import { ChevronDown } from 'lucide-react';

export default function Select({ label, error, className = '', id, children, ...props }) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-sm font-medium text-ink-soft">
          {label}
        </label>
      )}
      <div className="relative">
        <select
          id={id}
          className={`w-full appearance-none rounded-lg border bg-surface-2 px-3.5 py-2.5 pr-9 text-sm text-ink outline-none transition-colors focus:border-primary ${
            error ? 'border-error' : 'border-border'
          } ${className}`}
          {...props}
        >
          {children}
        </select>
        <ChevronDown
          size={16}
          className="pointer-events-none absolute right-3 top-1/2 -translate-y-1/2 text-ink-faint"
        />
      </div>
      {error && <span className="text-xs text-error">{error}</span>}
    </div>
  );
}
