import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';

const VARIANT_CLASSES = {
  primary: 'bg-primary hover:bg-primary-hover text-white',
  secondary: 'bg-surface-2 hover:bg-border text-ink border border-border',
  danger: 'bg-error hover:bg-red-600 text-white',
  ghost: 'bg-transparent hover:bg-surface-2 text-ink-soft hover:text-ink',
};

export default function Button({
  children,
  variant = 'primary',
  isLoading = false,
  disabled = false,
  className = '',
  type = 'button',
  ...props
}) {
  const spinnerClass = variant === 'primary' || variant === 'danger' ? 'text-white' : '';

  return (
    <button
      type={type}
      disabled={disabled || isLoading}
      className={`inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-sm font-medium transition-colors disabled:cursor-not-allowed disabled:opacity-50 ${VARIANT_CLASSES[variant]} ${className}`}
      {...props}
    >
      {isLoading && <LoadingSpinner size={16} className={spinnerClass} />}
      {children}
    </button>
  );
}
