/**
 * The PeerCode mark: screen, </> and stand.
 *
 * Drawn with `currentColor` rather than a fixed fill, so it takes its colour
 * from whatever it sits in - `className="text-primary"` tints it purple
 * exactly as the lucide icon it replaces did, and it will follow the theme if
 * that token ever changes.
 *
 * Stroke widths are scaled to lucide's visual weight so it does not look
 * heavier or lighter than the icons beside it in the navbar.
 */
export default function PeerCodeLogo({ size = 20, className = '', ...props }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      fill="none"
      stroke="currentColor"
      strokeLinecap="round"
      strokeLinejoin="round"
      role="img"
      aria-label="PeerCode"
      className={className}
      {...props}
    >
      <rect x="3.4" y="4.6" width="25.2" height="17.4" rx="3.6" strokeWidth="2.3" />
      <g strokeWidth="2.2">
        <path d="M13.6 9.9 10.6 13.3l3 3.4" />
        <path d="M18.4 8.9 13.6 17.7" />
        <path d="M18.4 9.9l3 3.4-3 3.4" />
        <path d="M16 22v3.2" />
        <path d="M11 27h10" />
      </g>
    </svg>
  );
}
