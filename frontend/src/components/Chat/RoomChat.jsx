import { useState, useEffect, useRef, useCallback } from 'react';
import { Send, MessageSquareOff } from 'lucide-react';
import {
  ref,
  query,
  limitToLast,
  onChildAdded,
  onValue,
  push,
  serverTimestamp,
  off,
} from 'firebase/database';
import { getFirebaseDb, getFirebaseAuth } from '../../services/firebase';
import { useAuth } from '../../hooks/useAuth';
import LoadingSpinner from '../LoadingSpinner/LoadingSpinner';

// Enough backlog to follow a conversation without pulling an entire contest's
// transcript into memory on every mount.
const MESSAGE_LIMIT = 200;
const MAX_LENGTH = 1000;

/**
 * Realtime chat for one room, backed by the Firebase Realtime Database.
 *
 * Messages stream straight from Firebase rather than through Django, which is
 * what makes them realtime. Authorisation is not this component's job: the
 * database rules only admit a uid present in the room's member index, and that
 * index is written solely by the backend when someone joins.
 */
export default function RoomChat({ roomCode }) {
  const { user, isChatReady, isChatConfigured, chatError } = useAuth();
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState('');
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState('');
  const [isConnecting, setIsConnecting] = useState(true);

  // Compared against each message's uid to decide what is "mine". Usernames
  // would be ambiguous and are attacker-supplied in the message body.
  const currentUid = getFirebaseAuth()?.currentUser?.uid ?? null;

  const scrollRef = useRef(null);
  const isPinnedToBottom = useRef(true);

  useEffect(() => {
    if (!isChatReady || !roomCode) return undefined;

    const db = getFirebaseDb();
    if (!db) return undefined;

    const messagesRef = ref(db, `rooms/${roomCode}/messages`);
    // Push ids sort chronologically, so limiting by key is already "the most
    // recent N" - no index or orderByChild needed.
    const recent = query(messagesRef, limitToLast(MESSAGE_LIMIT));

    // onChildAdded fires once per existing message and then once per new one,
    // so the same handler covers backfill and live updates.
    const unsubscribeAdded = onChildAdded(
      recent,
      (snapshot) => {
        const value = snapshot.val();
        setMessages((prev) => {
          if (prev.some((m) => m.id === snapshot.key)) return prev;
          return [...prev, { id: snapshot.key, ...value }];
        });
        setIsConnecting(false);
      },
      (err) => {
        // Almost always a rules rejection, which means the member index has
        // no entry for this uid.
        setError(
          err?.code === 'PERMISSION_DENIED'
            ? 'You do not have access to this room’s chat. Try rejoining the room.'
            : 'Could not load chat messages.'
        );
        setIsConnecting(false);
      }
    );

    // onChildAdded never fires for an empty room, so this clears the spinner
    // in the case where there is simply nothing to show yet.
    const unsubscribeValue = onValue(
      recent,
      () => setIsConnecting(false),
      () => setIsConnecting(false)
    );

    return () => {
      unsubscribeAdded();
      unsubscribeValue();
      off(messagesRef);
    };
  }, [roomCode, isChatReady]);

  // Reset when moving between rooms, or the previous room's messages would
  // briefly appear under the new room's heading.
  useEffect(() => {
    setMessages([]);
    setIsConnecting(true);
    setError('');
  }, [roomCode]);

  // Follow new messages, but only while the reader is already at the bottom -
  // yanking the view down while someone reads back is worse than no autoscroll.
  useEffect(() => {
    if (!isPinnedToBottom.current || !scrollRef.current) return;
    scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages]);

  const handleScroll = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    const distanceFromBottom = el.scrollHeight - el.scrollTop - el.clientHeight;
    isPinnedToBottom.current = distanceFromBottom < 40;
  }, []);

  async function handleSend(event) {
    event.preventDefault();
    const text = draft.trim();
    if (!text || isSending) return;

    const db = getFirebaseDb();
    // Take the uid from the Firebase session rather than rebuilding it from
    // the profile: the rules compare against auth.uid, and the profile
    // endpoint does not even expose a user id to rebuild it from.
    const uid = getFirebaseAuth()?.currentUser?.uid;
    if (!db || !uid) {
      setError('Chat session is not ready yet.');
      return;
    }

    setIsSending(true);
    setError('');
    // Clear immediately so the input feels responsive; restored on failure.
    setDraft('');
    isPinnedToBottom.current = true;
    try {
      await push(ref(db, `rooms/${roomCode}/messages`), {
        uid,
        username: user?.username ?? 'unknown',
        text,
        // The rules require createdAt === now, so the timestamp has to come
        // from the server. A client clock would be rejected, and rightly so.
        createdAt: serverTimestamp(),
      });
    } catch (err) {
      setDraft(text);
      setError(
        err?.code === 'PERMISSION_DENIED'
          ? 'Your message was rejected. You may no longer be a member of this room.'
          : 'Could not send that message.'
      );
    } finally {
      setIsSending(false);
    }
  }

  if (!isChatConfigured) {
    return (
      <Notice
        title="Chat is unavailable"
        body="This deployment has no Firebase configuration, so room chat is switched off."
      />
    );
  }

  if (!isChatReady) {
    return (
      <Notice
        title="Chat is not connected"
        body={chatError || 'We could not open a chat session for your account.'}
      />
    );
  }

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div
        ref={scrollRef}
        onScroll={handleScroll}
        className="flex-1 space-y-3 overflow-y-auto p-4"
      >
        {isConnecting && (
          <span className="flex items-center gap-2 text-sm text-ink-soft">
            <LoadingSpinner size={14} />
            Connecting to chat…
          </span>
        )}

        {!isConnecting && messages.length === 0 && !error && (
          <p className="text-sm text-ink-faint">
            No messages yet. Say something to your opponents.
          </p>
        )}

        {messages.map((message) => (
          <Message
            key={message.id}
            message={message}
            isMine={message.uid === currentUid}
          />
        ))}
      </div>

      {error && (
        <p className="border-t border-border px-4 py-2 text-xs text-error">{error}</p>
      )}

      <form onSubmit={handleSend} className="flex gap-2 border-t border-border p-3">
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value.slice(0, MAX_LENGTH))}
          placeholder="Message the room…"
          aria-label="Message the room"
          className="min-w-0 flex-1 rounded-lg border border-border bg-surface-2 px-3 py-2 text-sm text-ink placeholder:text-ink-faint focus:border-primary focus:outline-none"
        />
        <button
          type="submit"
          disabled={!draft.trim() || isSending}
          aria-label="Send message"
          className="inline-flex shrink-0 items-center justify-center rounded-lg bg-primary px-3 py-2 text-white transition-colors hover:bg-primary-hover disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isSending ? <LoadingSpinner size={15} className="text-white" /> : <Send size={15} />}
        </button>
      </form>
    </div>
  );
}

function Message({ message, isMine }) {
  return (
    <div className="text-sm">
      <div className="mb-0.5 flex items-baseline gap-2">
        <span
          className={`text-xs font-semibold ${isMine ? 'text-primary' : 'text-ink'}`}
        >
          {isMine ? 'You' : message.username}
        </span>
        <span className="text-[11px] text-ink-faint">{formatTime(message.createdAt)}</span>
      </div>
      {/* Rendered as text, never as markup: this is other users' input. */}
      <p className="whitespace-pre-wrap break-words text-ink-soft">{message.text}</p>
    </div>
  );
}

function Notice({ title, body }) {
  return (
    <div className="flex h-full flex-col items-center justify-center gap-2 p-6 text-center">
      <MessageSquareOff size={22} className="text-ink-faint" />
      <p className="text-sm font-medium text-ink">{title}</p>
      <p className="max-w-sm text-xs leading-relaxed text-ink-soft">{body}</p>
    </div>
  );
}

function formatTime(timestamp) {
  // serverTimestamp() resolves to a number, but a message that has just been
  // written locally can briefly arrive before the server fills it in.
  if (typeof timestamp !== 'number') return '';
  return new Date(timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit',
  });
}
