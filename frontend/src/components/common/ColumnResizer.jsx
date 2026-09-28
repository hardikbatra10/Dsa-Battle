import { useRef, useState } from 'react';
import { clamp } from '../../hooks/useColumnWidths';

/**
 * A draggable divider between two columns.
 *
 * Owns no width itself: it reports the new width for the column it belongs to,
 * and the parent decides what to do with it. `sign` is -1 when the column
 * being sized sits to the *right* of the handle, so dragging left makes it
 * wider rather than narrower.
 *
 * Pointer events (rather than mouse events) so a trackpad, a touchscreen and a
 * stylus all behave the same, and pointer capture so a fast drag that leaves
 * the 6px handle keeps resizing instead of stopping dead.
 */
export default function ColumnResizer({
  value,
  min,
  max,
  sign = 1,
  onChange,
  onReset,
  label,
}) {
  const drag = useRef(null);
  const [isDragging, setIsDragging] = useState(false);

  function handlePointerDown(event) {
    // Stops the browser from starting a text selection mid-drag.
    event.preventDefault();
    event.currentTarget.setPointerCapture(event.pointerId);
    drag.current = { startX: event.clientX, startValue: value };
    setIsDragging(true);
  }

  function handlePointerMove(event) {
    if (!drag.current) return;
    const delta = (event.clientX - drag.current.startX) * sign;
    onChange(clamp(drag.current.startValue + delta, min, max));
  }

  function handlePointerUp(event) {
    if (!drag.current) return;
    drag.current = null;
    setIsDragging(false);
    try {
      event.currentTarget.releasePointerCapture(event.pointerId);
    } catch {
      // The pointer may already have been released; nothing to undo.
    }
  }

  function handleKeyDown(event) {
    const step = event.shiftKey ? 48 : 16;
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      onChange(clamp(value - step * sign, min, max));
    } else if (event.key === 'ArrowRight') {
      event.preventDefault();
      onChange(clamp(value + step * sign, min, max));
    } else if (event.key === 'Enter' && onReset) {
      event.preventDefault();
      onReset();
    }
  }

  return (
    <div
      role="separator"
      aria-orientation="vertical"
      aria-label={label}
      aria-valuenow={Math.round(value)}
      aria-valuemin={min}
      aria-valuemax={max}
      tabIndex={0}
      title={`${label} — drag to resize, double-click to reset`}
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={handlePointerUp}
      onPointerCancel={handlePointerUp}
      onDoubleClick={onReset}
      onKeyDown={handleKeyDown}
      className="group relative hidden w-1.5 shrink-0 cursor-col-resize touch-none select-none focus:outline-none lg:block"
    >
      {/* A 6px target is comfortable to grab, but a 6px line would be ugly,
          so only a hairline is painted until the handle is engaged. */}
      <span
        className={`absolute inset-y-0 left-1/2 w-px -translate-x-1/2 transition-colors ${
          isDragging
            ? 'bg-primary'
            : 'bg-border group-hover:bg-primary/60 group-focus:bg-primary/60'
        }`}
      />
    </div>
  );
}
