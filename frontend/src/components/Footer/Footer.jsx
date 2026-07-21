export default function Footer() {
  return (
    <footer className="border-t border-border py-6">
      <div className="mx-auto max-w-6xl px-4 text-center text-xs text-ink-faint sm:px-6">
        © {new Date().getFullYear()}  PeerCode — competitive coding, with friends.
      </div>
    </footer>
  );
}
