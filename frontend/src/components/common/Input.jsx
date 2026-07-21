export default function Input({ label, error, className = '', id, ...props }) {
  return (
    <div className="flex flex-col gap-1.5">
      {label && (
        <label htmlFor={id} className="text-sm font-medium text-ink-soft">
          {label}
        </label>
      )}
      <input
        id={id}
        className={`w-full rounded-lg border bg-surface-2 px-3.5 py-2.5 text-sm text-ink outline-none transition-colors placeholder:text-ink-faint focus:border-primary ${
          error ? 'border-error' : 'border-border'
        } ${className}`}
        {...props}
      />
      {error && <span className="text-xs text-error">{error}</span>}
    </div>
  );
}
