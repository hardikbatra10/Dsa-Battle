import { useEffect } from 'react';

/**
 * A centred dialog over a dimmed backdrop.
 *
 * `onClose` is optional: an announcement the user must acknowledge can omit
 * it, and the dialog then has no backdrop-click or Escape dismissal, leaving
 * whatever action buttons the caller puts in `children` as the only way out.
 */
export default function Modal({ open, title, icon, onClose, children }) {
  useEffect(() => {
    if (!open || !onClose) return undefined;
    function onKeyDown(event) {
      if (event.key === 'Escape') onClose();
    }
    document.addEventListener('keydown', onKeyDown);
    return () => document.removeEventListener('keydown', onKeyDown);
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-4"
      onClick={onClose ? () => onClose() : undefined}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label={title}
        // Without this the click would bubble to the backdrop and close the
        // dialog the moment anyone clicked inside it.
        onClick={(event) => event.stopPropagation()}
        className="w-full max-w-md rounded-xl border border-border bg-surface p-6 shadow-xl"
      >
        <div className="mb-3 flex items-center gap-2.5">
          {icon}
          <h2 className="text-base font-semibold text-ink">{title}</h2>
        </div>
        {children}
      </div>
    </div>
  );
}
