import { useState, useEffect, useMemo, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Send, Play, CheckCircle2, XCircle, Square, Flag,
  MessageSquare, PanelRightClose, LogOut,
} from 'lucide-react';
import { getRoom, endRoom, getLeaderboard } from '../api/rooms';
import { listProblems } from '../api/problems';
import { submitSolution, runSolution, getSubmissionHistory } from '../api/submissions';
import { getApiErrorMessage } from '../api/axios';
import { useAuth } from '../hooks/useAuth';
import { usePolling } from '../hooks/usePolling';
import { LANGUAGE_LABELS, VERDICT_LABELS } from '../utils/formatters';
import ContestLayout from '../layouts/ContestLayout';
import ContestTimer from '../components/ContestTimer/ContestTimer';
import ProblemSidebar from '../components/Sidebar/ProblemSidebar';
import ProblemCard from '../components/ProblemCard/ProblemCard';
import CodeEditor from '../components/CodeEditor/CodeEditor';
import Leaderboard from '../components/Leaderboard/Leaderboard';
import RoomChat from '../components/Chat/RoomChat';
import Select from '../components/common/Select';
import Button from '../components/common/Button';
import ErrorBanner from '../components/common/ErrorBanner';
import Modal from '../components/common/Modal';
import LoadingSpinner from '../components/LoadingSpinner/LoadingSpinner';
import TestCaseResult from '../components/common/TestCaseResult';

const ROOM_POLL_MS = 5000;
const LEADERBOARD_POLL_MS = 6000;
const CODE_STORAGE_PREFIX = 'dsa_battle_code_';
const CHAT_OPEN_KEY = 'dsa_battle_chat_open';

export default function Contest() {
  const { roomCode } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  const [room, setRoom] = useState(null);
  const [allProblems, setAllProblems] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState('');

  const [activeProblemId, setActiveProblemId] = useState(null);
  const [tab, setTab] = useState('problem');
  const [solvedProblemIds, setSolvedProblemIds] = useState(new Set());
  const [codeByProblem, setCodeByProblem] = useState({});
  const [languageByProblem, setLanguageByProblem] = useState({});
  const [verdictByProblem, setVerdictByProblem] = useState({});
  const [failureByProblem, setFailureByProblem] = useState({});
  const [runResultByProblem, setRunResultByProblem] = useState({});

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [runError, setRunError] = useState('');
  const [isExpiredLocally, setIsExpiredLocally] = useState(false);
  const [hasSeenEndNotice, setHasSeenEndNotice] = useState(false);
  // Chat is always present, but collapsible: on a narrow laptop a permanent
  // third column leaves the editor too cramped to work in.
  const [isChatOpen, setIsChatOpen] = useState(
    () => localStorage.getItem(CHAT_OPEN_KEY) !== 'false'
  );

  useEffect(() => {
    localStorage.setItem(CHAT_OPEN_KEY, String(isChatOpen));
  }, [isChatOpen]);
  const [isEnding, setIsEnding] = useState(false);

  // Initial load: room, the full problem bank (there's no "get problem by id"
  // endpoint, so we fetch everything and match by id) and this user's own
  // submissions for this room, to know which problems are already solved.
  useEffect(() => {
    let cancelled = false;

    async function load() {
      setIsLoading(true);
      setLoadError('');
      try {
        const [roomRes, problemsRes, historyRes] = await Promise.all([
          getRoom(roomCode),
          listProblems(),
          getSubmissionHistory(roomCode, { mine: true }),
        ]);
        if (cancelled) return;

        setRoom(roomRes.data);
        setAllProblems(problemsRes.data);

        // SubmissionHistorySerializer doesn't expose a problem id, only
        // problem_title. Problem.title is unique on the backend, so matching
        // on title is a safe way to recover which problems are solved.
        const titleToId = new Map(
          problemsRes.data.map((problem) => [problem.title, problem.id])
        );
        const solved = new Set();
        historyRes.data.forEach((submission) => {
          if (submission.verdict === 'accepted' && titleToId.has(submission.problem_title)) {
            solved.add(titleToId.get(submission.problem_title));
          }
        });
        setSolvedProblemIds(solved);

        const saved = localStorage.getItem(`${CODE_STORAGE_PREFIX}${roomCode}`);
        if (saved) {
          try {
            const parsed = JSON.parse(saved);
            setCodeByProblem(parsed.codeByProblem || {});
            setLanguageByProblem(parsed.languageByProblem || {});
          } catch {
            // ignore malformed local storage content
          }
        }
      } catch (err) {
        if (!cancelled) setLoadError(getApiErrorMessage(err, 'Could not load this contest.'));
      } finally {
        if (!cancelled) setIsLoading(false);
      }
    }

    load();
    return () => {
      cancelled = true;
    };
  }, [roomCode]);

  // Problems belonging to this room, in the order the backend returned them.
  const roomProblems = useMemo(() => {
    if (!room) return [];
    return room.selected_problems
      .map((id) => allProblems.find((problem) => problem.id === id))
      .filter(Boolean);
  }, [room, allProblems]);

  useEffect(() => {
    if (roomProblems.length && activeProblemId === null) {
      setActiveProblemId(roomProblems[0].id);
    }
  }, [roomProblems, activeProblemId]);

  // Persist in-progress code locally so a refresh mid-contest doesn't wipe it.
  useEffect(() => {
    localStorage.setItem(
      `${CODE_STORAGE_PREFIX}${roomCode}`,
      JSON.stringify({ codeByProblem, languageByProblem })
    );
  }, [roomCode, codeByProblem, languageByProblem]);

  // A room that hasn't been started yet has no business being on this page.
  useEffect(() => {
    if (room && room.status === 'waiting') {
      navigate(`/rooms/${roomCode}`, { replace: true });
    }
  }, [room, roomCode, navigate]);

  const isCreator = room && room.creator_username === user?.username;
  const isContestOver = room?.status === 'finished' || isExpiredLocally;

  // Deliberately no forced tab switch here. The end-of-contest dialog
  // announces the result and offers the leaderboard; dragging someone off
  // the problem they were midway through would defeat the whole point of
  // letting them carry on.

  const refreshRoom = useCallback(async () => {
    try {
      const { data } = await getRoom(roomCode);
      setRoom(data);
    } catch {
      // transient polling failure, ignore and try again next tick
    }
  }, [roomCode]);

  const refreshLeaderboard = useCallback(async () => {
    try {
      const { data } = await getLeaderboard(roomCode);
      setLeaderboard(data);
    } catch {
      // transient polling failure, ignore and try again next tick
    }
  }, [roomCode]);

  usePolling(refreshRoom, ROOM_POLL_MS, room?.status === 'active');
  usePolling(refreshLeaderboard, LEADERBOARD_POLL_MS, !!room && room.status !== 'waiting');

  // The room stays "active" server-side until something explicitly ends it.
  // Rather than leave that to the creator remembering to click "End Room",
  // the creator's own client closes it out the moment the clock hits zero —
  // every other participant then picks up status "finished" on their next
  // room poll and gets redirected below.
  async function handleTimerExpire() {
    setIsExpiredLocally(true);
    if (isCreator && room?.status === 'active') {
      try {
        await endRoom(roomCode);
      } catch {
        // already ended by someone else (e.g. a late submission attempt) — ignore
      }
    }
    refreshRoom();
  }

  // When the contest ends the page stays exactly where it is. Nobody is
  // redirected: the dialog below says the scoring window has closed, and
  // everyone is free to keep working on the problems afterwards.
  const showEndNotice = isContestOver && !hasSeenEndNotice;

  async function handleEndRoom() {
    if (!window.confirm('End this room for everyone? This cannot be undone.')) return;
    setIsEnding(true);
    try {
      await endRoom(roomCode);
      await refreshRoom();
    } catch (err) {
      setSubmitError(getApiErrorMessage(err, 'Could not end the room.'));
    } finally {
      setIsEnding(false);
    }
  }

  async function handleSubmit() {
    if (!activeProblemId) return;
    setSubmitError('');
    setIsSubmitting(true);
    try {
      const { data } = await submitSolution({
        room: room.id,
        problem: activeProblemId,
        code: codeByProblem[activeProblemId] || '',
        language: languageByProblem[activeProblemId] || 'cpp',
      });
      setVerdictByProblem((prev) => ({ ...prev, [activeProblemId]: data.verdict }));
      setFailureByProblem((prev) => ({ ...prev, [activeProblemId]: data.failure_detail || null }));
      if (data.verdict === 'accepted') {
        setSolvedProblemIds((prev) => new Set(prev).add(activeProblemId));
      }
    } catch (err) {
      setSubmitError(getApiErrorMessage(err, 'Submission failed.'));
      // The backend authoritatively rejects late submissions; if that's why
      // this failed, sync our local view of the room's status.
      refreshRoom();
    } finally {
      setIsSubmitting(false);
    }
  }

  async function handleRun() {
    if (!activeProblemId) return;
    setRunError('');
    setIsRunning(true);
    try {
      const { data } = await runSolution({
        room: room.id,
        problem: activeProblemId,
        code: codeByProblem[activeProblemId] || '',
        language: languageByProblem[activeProblemId] || 'cpp',
      });
      setRunResultByProblem((prev) => ({ ...prev, [activeProblemId]: data }));
    } catch (err) {
      setRunError(getApiErrorMessage(err, 'Run failed.'));
    } finally {
      setIsRunning(false);
    }
  }

  if (isLoading) {
    return (
      <ContestLayout roomCode={roomCode}>
        <div className="flex h-full items-center justify-center">
          <LoadingSpinner size={28} />
        </div>
      </ContestLayout>
    );
  }

  if (loadError || !room) {
    return (
      <ContestLayout roomCode={roomCode}>
        <div className="mx-auto max-w-md p-6">
          <ErrorBanner message={loadError || 'Contest not found.'} />
        </div>
      </ContestLayout>
    );
  }

  const activeProblem = roomProblems.find((problem) => problem.id === activeProblemId);
  const activeCode = codeByProblem[activeProblemId] ?? '';
  const activeLanguage = languageByProblem[activeProblemId] ?? 'cpp';
  const activeVerdict = verdictByProblem[activeProblemId];
  const activeFailure = failureByProblem[activeProblemId];
  const activeRunResult = runResultByProblem[activeProblemId];

  return (
    <ContestLayout
      roomCode={roomCode}
      timerSlot={
        room.started_at && (
          <ContestTimer
            startedAt={room.started_at}
            timeLimitMinutes={room.time_limit_minutes}
            onExpire={handleTimerExpire}
          />
        )
      }
    >
      <div className="flex h-full flex-col lg:flex-row">
        <aside className="shrink-0 overflow-y-auto border-b border-border lg:w-60 lg:border-b-0 lg:border-r">
          <ProblemSidebar
            problems={roomProblems}
            activeProblemId={activeProblemId}
            solvedProblemIds={solvedProblemIds}
            onSelect={setActiveProblemId}
          />
          {isCreator && room.status === 'active' && (
            <div className="border-t border-border p-3">
              <Button variant="danger" onClick={handleEndRoom} isLoading={isEnding} className="w-full text-xs">
                <Square size={13} />
                End Room
              </Button>
            </div>
          )}

          {/* Once the contest is over nobody is forced out, so leaving needs
              an explicit way back. This only navigates: the user stays a
              participant, so the final standings and their room history are
              unaffected by walking away. */}
          {isContestOver && (
            <div className="border-t border-border p-3">
              <Button
                variant="danger"
                onClick={() => navigate('/dashboard')}
                className="w-full text-xs"
              >
                <LogOut size={13} />
                Exit Room
              </Button>
            </div>
          )}
        </aside>

        <section className="flex min-h-0 flex-1 flex-col overflow-y-auto border-b border-border lg:w-[26rem] lg:flex-none lg:border-b-0 lg:border-r">
          <div className="flex border-b border-border">
            <TabButton active={tab === 'problem'} onClick={() => setTab('problem')}>
              Problem
            </TabButton>
            <TabButton active={tab === 'leaderboard'} onClick={() => setTab('leaderboard')}>
              Leaderboard
            </TabButton>
          </div>
          <div className="flex-1 overflow-y-auto p-5">
            {isContestOver && (
              <div className="mb-4 flex items-start gap-2 rounded-lg border border-border bg-surface-2 px-3.5 py-2.5 text-sm text-ink-soft">
                <Flag size={16} className="mt-0.5 shrink-0 text-ink-faint" />
                <span>
                  Contest ended. You can keep solving these problems, but new submissions
                  are no longer counted towards the leaderboard.
                </span>
              </div>
            )}
            {tab === 'problem' ? (
              <ProblemCard problem={activeProblem} />
            ) : (
              <Leaderboard entries={leaderboard} currentUsername={user?.username} />
            )}
          </div>
        </section>

        <section className="flex min-h-[420px] flex-1 flex-col">
          <div className="flex items-center justify-between gap-3 border-b border-border px-4 py-2">
            <Select
              value={activeLanguage}
              onChange={(event) =>
                setLanguageByProblem((prev) => ({ ...prev, [activeProblemId]: event.target.value }))
              }
              className="w-36 py-2 text-xs"
            >
              {Object.entries(LANGUAGE_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </Select>
            <div className="flex items-center gap-2">
              <Button
                variant="secondary"
                onClick={handleRun}
                isLoading={isRunning}
                disabled={!activeProblemId || isSubmitting}
              >
                <Play size={15} />
                Run
              </Button>
              <Button
                onClick={handleSubmit}
                isLoading={isSubmitting}
                disabled={!activeProblemId || isRunning}
              >
                <Send size={15} />
                {isContestOver ? 'Submit (not counted)' : 'Submit Solution'}
              </Button>
            </div>
          </div>

          <div className="min-h-0 flex-1">
            <CodeEditor
              language={activeLanguage}
              value={activeCode}
              onChange={(value) =>
                setCodeByProblem((prev) => ({ ...prev, [activeProblemId]: value }))
              }
            />
          </div>

          {(isRunning || runError || activeRunResult || isSubmitting || activeVerdict || submitError) && (
            <div className="flex max-h-72 flex-col gap-4 overflow-y-auto border-t border-border p-4">
              {(isRunning || runError || activeRunResult) && (
                <div>
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink-faint">
                    Sample Run
                  </p>
                  {isRunning && (
                    <span className="flex items-center gap-2 text-sm text-ink-soft">
                      <LoadingSpinner size={14} />
                      Running sample test cases…
                    </span>
                  )}
                  {!isRunning && runError && <ErrorBanner message={runError} />}
                  {!isRunning && !runError && activeRunResult && (
                    <div className="flex flex-col gap-2">
                      {activeRunResult.results.map((result, index) => (
                        <TestCaseResult key={index} result={result} label={`Sample ${index + 1}`} />
                      ))}
                    </div>
                  )}
                </div>
              )}

              {(isSubmitting || activeVerdict || submitError) && (
                <div>
                  <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-ink-faint">
                    Submission Result
                  </p>
                  {isSubmitting && (
                    <span className="flex items-center gap-2 text-sm text-ink-soft">
                      <LoadingSpinner size={14} />
                      Judging against hidden test cases…
                    </span>
                  )}
                  {!isSubmitting && submitError && <ErrorBanner message={submitError} />}
                  {!isSubmitting && !submitError && activeVerdict && (
                    <div className="flex flex-col gap-2">
                      <VerdictBanner verdict={activeVerdict} />
                      {activeFailure && (
                        <TestCaseResult
                          result={{ ...activeFailure, passed: false, verdict: activeVerdict }}
                        />
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </section>

        {/* Chat lives here rather than behind a tab so it is visible the whole
            time, the way a voice channel would be. On screens below lg the
            row stacks, so this becomes a panel underneath the editor. */}
        <aside
          className={`flex shrink-0 flex-col border-t border-border lg:border-l lg:border-t-0 ${
            isChatOpen ? 'h-72 lg:h-auto lg:w-80' : 'lg:w-12'
          }`}
        >
          <div className="flex items-center justify-between gap-2 border-b border-border px-3 py-2.5">
            {isChatOpen && (
              <h2 className="text-xs font-semibold uppercase tracking-wide text-ink-faint">
                Room chat
              </h2>
            )}
            <button
              type="button"
              onClick={() => setIsChatOpen((open) => !open)}
              aria-label={isChatOpen ? 'Hide room chat' : 'Show room chat'}
              title={isChatOpen ? 'Hide chat' : 'Show chat'}
              className="ml-auto rounded-md p-1 text-ink-faint transition-colors hover:bg-surface-2 hover:text-ink"
            >
              {isChatOpen ? <PanelRightClose size={16} /> : <MessageSquare size={16} />}
            </button>
          </div>

          {isChatOpen && (
            <div className="min-h-0 flex-1">
              <RoomChat roomCode={roomCode} />
            </div>
          )}
        </aside>
      </div>

      <Modal
        open={showEndNotice}
        title="Contest has ended"
        icon={<Flag size={18} className="text-ink-faint" />}
        onClose={() => setHasSeenEndNotice(true)}
      >
        <p className="text-sm leading-relaxed text-ink-soft">
          The scoring window for this room is closed, and the leaderboard is final.
          Submissions from now on will not be counted.
        </p>
        <p className="mt-3 text-sm leading-relaxed text-ink-soft">
          You can stay and keep working through the problems for practice - your
          code is still run and judged, it just no longer affects the standings.
        </p>
        <div className="mt-6 flex flex-wrap justify-end gap-2">
          <Button variant="ghost" onClick={() => navigate('/dashboard')}>
            Back to dashboard
          </Button>
          <Button
            variant="secondary"
            onClick={() => {
              setHasSeenEndNotice(true);
              setTab('leaderboard');
            }}
          >
            View final standings
          </Button>
          <Button onClick={() => setHasSeenEndNotice(true)}>Keep practising</Button>
        </div>
      </Modal>
    </ContestLayout>
  );
}

function TabButton({ active, onClick, children }) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex-1 border-b-2 px-4 py-2.5 text-sm font-medium transition-colors ${
        active ? 'border-primary text-primary' : 'border-transparent text-ink-soft hover:text-ink'
      }`}
    >
      {children}
    </button>
  );
}

function VerdictBanner({ verdict }) {
  const isAccepted = verdict === 'accepted';
  const toneClass = isAccepted
    ? 'border-success/30 bg-success-soft text-success'
    : 'border-error/30 bg-error-soft text-error';

  return (
    <div className={`flex items-center gap-2 rounded-lg border px-3.5 py-2.5 text-sm font-medium ${toneClass}`}>
      {isAccepted ? <CheckCircle2 size={16} /> : <XCircle size={16} />}
      {VERDICT_LABELS[verdict] || verdict}
    </div>
  );
}
