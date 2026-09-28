import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'dsa_battle_contest_columns';

// Widths in pixels. The defaults match what the layout used when the columns
// were fixed (w-60 / 26rem / w-80), so an existing user sees no jump.
export const COLUMN_DEFAULTS = { sidebar: 240, panel: 416, chat: 320 };

export const COLUMN_LIMITS = {
  sidebar: { min: 150, max: 440 },
  panel: { min: 260, max: 760 },
  chat: { min: 200, max: 560 },
};

// The editor is the column with no width of its own - it takes what is left.
// Every resize is clamped so this much always remains for it, otherwise a
// determined drag could squeeze the code editor out of existence.
export const EDITOR_MIN = 300;

const WIDE_QUERY = '(min-width: 1024px)';

export function clamp(value, min, max) {
  return Math.min(Math.max(value, min), Math.max(min, max));
}

function readStored() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY) || '');
    if (!parsed || typeof parsed !== 'object') return COLUMN_DEFAULTS;
    // Only take keys we recognise, and only if they are usable numbers - a
    // hand-edited or stale entry should not be able to break the layout.
    return Object.fromEntries(
      Object.entries(COLUMN_DEFAULTS).map(([key, fallback]) => {
        const value = parsed[key];
        const ok = typeof value === 'number' && Number.isFinite(value);
        const limits = COLUMN_LIMITS[key];
        return [key, ok ? clamp(value, limits.min, limits.max) : fallback];
      })
    );
  } catch {
    return COLUMN_DEFAULTS;
  }
}

/**
 * Column widths for the contest layout, remembered per browser.
 *
 * Only meaningful on wide screens: below the lg breakpoint the columns stack
 * vertically, where a horizontal width would be meaningless, so `isWide` tells
 * callers whether to apply the widths and show the drag handles at all.
 */
export function useColumnWidths() {
  const [widths, setWidths] = useState(readStored);
  const [isWide, setIsWide] = useState(
    () => typeof window !== 'undefined' && window.matchMedia(WIDE_QUERY).matches
  );

  useEffect(() => {
    const query = window.matchMedia(WIDE_QUERY);
    const onChange = (event) => setIsWide(event.matches);
    query.addEventListener('change', onChange);
    return () => query.removeEventListener('change', onChange);
  }, []);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(widths));
    } catch {
      // A browser with storage blocked still resizes, it just forgets.
    }
  }, [widths]);

  const setWidth = useCallback((key, value) => {
    setWidths((prev) => ({ ...prev, [key]: Math.round(value) }));
  }, []);

  const resetWidths = useCallback(() => setWidths(COLUMN_DEFAULTS), []);

  return { widths, setWidth, resetWidths, isWide };
}
