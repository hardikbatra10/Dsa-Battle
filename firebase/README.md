# Firebase setup

Room chat and Google sign-in both run through one Firebase project. Nothing in
this repo can create that project for you, so this is the manual part.

**No service account key is used anywhere.** The backend's only Firebase job is
to verify Google sign-in tokens, and that needs nothing but Google's public
certificates plus the project id. See "What this costs" below for what is given
up in exchange.

## Provisioning

1. Create a project at <https://console.firebase.google.com>.
2. **Realtime Database** → Create database. Pick a region, and start in
   **locked mode** — the rules below replace the default anyway.
3. **Build → Realtime Database → Rules**: paste `database.rules.json` and
   publish. Or, with the Firebase CLI: `firebase deploy --only database`.
4. **Authentication → Sign-in method** → enable **Google**, and also enable
   **Anonymous** (see below for why).
5. Same screen, **Authorized domains**: add `localhost` and your Vercel
   domain. Google sign-in fails on an unlisted domain even with a correct
   config.
6. **Project settings → General → Your apps** → add a **Web app**, and copy
   the config into `frontend/.env` (see `frontend/.env.example`). Those values
   are public by design: they identify the project, they do not authorise
   anything. `database.rules.json` is what actually protects the data.
7. Backend: set `FIREBASE_PROJECT_ID` to the project id. That is the only
   Firebase variable the backend reads.

## Where the chats are stored

Keyed by room code, one child per message:

```
/rooms/{roomCode}/messages/{pushId}
    uid        the sender's Firebase uid
    username   display name, shown in the transcript
    text       the message, 1-1000 characters
    createdAt  server timestamp
```

Push ids sort chronologically, so "the most recent N messages" is a plain
`limitToLast` with no index needed.

## What the rules enforce

`database.rules.json` is the whole authorisation story, because browsers talk
to the database directly. Read it as four claims:

1. **Nothing is world-readable.** The root denies everything and only the
   paths below re-grant access, so a path nobody thought about stays shut.
2. **You must be signed in.** `auth != null` for both read and write.
3. **Messages are append-only and unforgeable.** `!data.exists()` means an
   existing message can never be edited or deleted, by its author or anyone
   else. `uid === auth.uid` means you cannot post under another uid, and
   `createdAt === now` means you cannot backdate.
4. **Nothing extra can be smuggled in.** `$other: {".validate": false}`
   rejects any field the schema does not name.

## Two identity paths

Django stays the source of truth for accounts. Firebase never owns one.

```
Google popup ──► Firebase ID token ──► POST /api/users/google/
                                          │ verified against Google's PUBLIC
                                          │ certs; finds or creates the Django
                                          │ user by verified email
                                          ▼
                                    Django JWT (access + refresh)

Firebase session for chat:
  signed in with Google  ──► the popup's own session is kept (stable uid)
  signed in with a password ──► signInAnonymously() (per-browser uid)
```

A password user has no Google identity to reuse, and giving them one tied to
their Django account would need a service account key to mint a custom token.
They get an anonymous Firebase session instead, which is why **Anonymous** has
to be enabled in step 4. Chat works the same either way.

## What this costs

Running keyless has two consequences, both deliberate:

- **Chat is not restricted to a room's participants.** Enforcing that would
  need a server-written index of who is in which room, which needs a key. As
  written, any signed-in user who knows a room code can read and post in that
  room's chat. Room codes are 8 hex characters and are shared openly with
  participants, so treat room chat as semi-public rather than confidential.
- **Display names are self-reported.** `uid` is guaranteed by the rules, but
  `username` is whatever the client sends, so one user could post under
  another's name. Nothing that matters is decided by chat, but do not read the
  transcript as an audit trail.

If either becomes a problem, the fix is a service account key plus a
membership index the rules check — roughly the diff this file used to describe.

## If Firebase is not configured

The app degrades rather than breaks. Rooms, judging and the leaderboard never
touch Firebase at all. `POST /api/users/google/` returns **503** with a clear
message, and the chat panel renders an explanation instead of a broken input.
