# DSA Battle — Frontend

A React + Vite frontend for DSA Battle, a multiplayer competitive coding platform. It talks to the
existing Django REST Framework backend in `../backend` — this app does not implement any game logic
itself, it's purely a client for that API.

## 1. Install dependencies

```bash
cd frontend
npm install
```

## 2. Configure environment variables

Copy the example file and adjust if your Django server runs somewhere other than
`http://127.0.0.1:8000`:

```bash
cp .env.example .env
```

```
VITE_API_BASE_URL=http://127.0.0.1:8000
```

The frontend appends `/api` itself, so `VITE_API_BASE_URL` should just be the host — see
`src/api/axios.js`.

## 3. Run the dev server

```bash
npm run dev
```

The app runs on **http://localhost:3000**. This port is intentional: the backend's
`CORS_ALLOWED_ORIGINS` (`backend/config/settings.py`) only allows `http://localhost:3000`, so the
dev server is pinned to that port in `vite.config.js`.

Make sure the Django backend is running separately (`python manage.py runserver`, default port
8000) and that Postgres is reachable and migrated.

## 4. Folder structure

```
src/
├── api/            axios instance + one thin file per backend app (auth, rooms, problems, submissions)
├── components/      reusable UI, grouped by feature (Navbar, Sidebar, CodeEditor, Leaderboard,
│                    ContestTimer, SubmissionCard, LoadingSpinner) plus components/common (Button,
│                    Input, Select, Card, Badge, EmptyState, ErrorBanner)
├── context/          AuthContext — the single source of truth for "who is logged in"
├── hooks/            useAuth (re-exports AuthContext's hook), usePolling (generic interval hook)
├── layouts/          MainLayout (navbar + footer chrome) and ContestLayout (full-height, no chrome)
├── pages/            one file per route
├── routes/           ProtectedRoute — redirects to /login if there's no session
├── utils/            token.js (localStorage helpers), formatters.js (labels, dates, mm:ss)
├── App.jsx           react-router-dom route tree
└── main.jsx          React root
```

## 5. How authentication works

- `POST /api/token/` returns `{ access, refresh }`. Both are stored in `localStorage`
  (`src/utils/token.js`).
- Every request made through the shared axios instance (`src/api/axios.js`) automatically attaches
  `Authorization: Bearer <access>`.
- On a 401, the axios response interceptor calls `POST /api/token/refresh/` once, retries the
  original request with the new access token, and only gives up (clearing tokens + logging out) if
  the refresh itself fails.
- `AuthContext` (`src/context/AuthContext.jsx`) loads `GET /api/users/profile/` on startup if a
  token exists, so refreshing the page doesn't log you out. It exposes `user`, `isAuthenticated`,
  `login()`, `register()`, `logout()`.
- `ProtectedRoute` (`src/routes/ProtectedRoute.jsx`) wraps every private route and redirects to
  `/login` when `isAuthenticated` is false.

## 6. How Axios talks to Django

```
Page component → api/<resource>.js function → shared axios instance (src/api/axios.js) → DRF
```

Each `api/*.js` file is a thin wrapper around one Django app's endpoints — no raw `axios.get(...)`
calls happen inside components. `getApiErrorMessage()` in `api/axios.js` extracts the actual DRF
error message (`{"error": "..."}`, `{"detail": "..."}`, or field-level validation errors) so the UI
always shows the backend's real message instead of a generic one.

## 7. Major routes

| Route | Purpose |
|---|---|
| `/login`, `/register` | Auth |
| `/dashboard` | Landing page after login: create/join room, quick stats |
| `/rooms/create`, `/rooms/join` | Room creation / joining forms |
| `/rooms/:roomCode` | Lobby — participants, status, Start/Leave Room |
| `/rooms/:roomCode/contest` | The coding interface (Monaco editor, submissions) |
| `/rooms/:roomCode/leaderboard` | Standalone leaderboard view |
| `/rooms/:roomCode/submissions` | Submission history (All / Mine) |
| `/submissions/:submissionId` | One submission's full code + verdict |
| `/profile` | User stats |

## 8. Contest flow

1. Creator calls **Create Room** → backend randomly assigns `number_of_questions` problems matching
   the chosen topic/difficulty and returns a `room_code`.
2. Everyone lands in the **Lobby** (`/rooms/:roomCode`), which polls `GET /api/rooms/:roomCode/`
   every 3s.
3. Creator clicks **Start Room** → backend sets `status: "active"` and `started_at`. Every
   participant's poll picks this up and auto-navigates them to `/rooms/:roomCode/contest`.
4. On the contest page, `ContestTimer` computes `started_at + time_limit_minutes` locally and counts
   down — it never polls just to tick a clock. The backend independently re-validates the deadline
   on every submission, so the timer is a display aid, not the source of truth.
5. Submitting a solution disables the button, shows "Judging…", then displays the returned verdict
   (Accepted / Wrong Answer / etc.) via `POST /api/submissions/submit/`.
6. The contest ends either when the timer hits zero locally (submissions are disabled client-side;
   the backend rejects them regardless) or when the creator calls **End Room**
   (`POST /api/rooms/:roomCode/end/`).
7. The Leaderboard tab (and the standalone `/leaderboard` page) polls
   `GET /api/rooms/:roomCode/leaderboard/`.

## 9. Monaco Editor integration

`src/components/CodeEditor/CodeEditor.jsx` wraps `@monaco-editor/react`. The contest page
(`src/pages/Contest.jsx`) keeps one code string and one language per problem in React state
(`codeByProblem`, `languageByProblem`), so switching between problems A/B/C doesn't lose your work.
That state is also mirrored into `localStorage` (keyed by room code) so a refresh mid-contest
doesn't wipe it either — it's a local convenience only, the backend is unaffected. Submitting sends
`{ room: <room's numeric id>, problem: <problem id>, code, language }` to
`POST /api/submissions/submit/`; note it's the room's **database id**, not its `room_code` — that's
what `SubmissionSerializer` expects.

## 10. Known backend constraints this frontend works around

- `Submission.LANGUAGE_CHOICES` includes `javascript`, but the Judge0 service has no mapping for it
  and would 500. The language picker only offers C++, Java and Python.
- `SubmissionHistorySerializer` returns `problem_title` but not a problem id. Since `Problem.title`
  is unique on the backend, the contest page matches submissions back to problems by title to know
  which ones are already solved.
- There's no "get one problem by id" endpoint, so the contest page fetches the full problem list
  (`GET /api/problems/`) once and filters client-side by the room's `selected_problems` ids.

## Backend changes made alongside this frontend

A few backend fixes were necessary for the frontend to function at all — flagged and approved
before making them:

- `submissions/urls.py` referenced `SubmissionDetailView` without importing it, which crashed the
  entire Django app on startup. Fixed the import.
- `rooms/urls.py` didn't register the already-implemented `LeaveRoomView` / `LeaderboardView`.
  Wired up `/rooms/<room_code>/leave/` and `/rooms/<room_code>/leaderboard/`.
- `RoomSerializer` didn't expose `status`, `started_at`, or `ended_at`, which the lobby and contest
  timer both need. Added as read-only fields.
- `RoomSerializer` only exposed `creator`/`participants` as raw numeric user ids, and no endpoint
  told the frontend its own user id — making it impossible to detect "am I the room creator" to
  gate the Start/End Room buttons. Added read-only `creator_username` and `participant_usernames`.

No existing field, endpoint, or request/response shape was changed — everything above is additive.
