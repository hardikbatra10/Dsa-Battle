import { Link } from 'react-router-dom';
import { Swords, Users, Trophy, Timer, Code2, ListChecks, CheckCircle2, ArrowRight } from 'lucide-react';
import Button from '../components/common/Button';
import Card from '../components/common/Card';
import { Badge, DifficultyBadge } from '../components/common/Badge';

const FEATURES = [
  {
    icon: Users,
    title: 'Private Rooms',
    description: 'Create a room and share the code, or drop into a friend’s with theirs — no public matchmaking noise.',
  },
  {
    icon: Timer,
    title: 'Timed Contests',
    description: 'Every battle runs on the clock. Solve as many problems as you can before time runs out.',
  },
  {
    icon: Code2,
    title: 'Real Code Editor',
    description: 'Write and run C++, Java or Python in a full editor, judged instantly against real test cases.',
  },
  {
    icon: Trophy,
    title: 'Live Leaderboard',
    description: 'Watch ranks update in real time as everyone in the room submits solutions.',
  },
  {
    icon: ListChecks,
    title: 'Curated Problems',
    description: 'Arrays to graphs to DP — pick topics and difficulty that match what you’re training for.',
  },
  {
    icon: CheckCircle2,
    title: 'Instant Verdicts',
    description: 'Accepted, wrong answer, TLE — know exactly where your solution stands the moment you submit.',
  },
];

const STEPS = [
  {
    step: '1',
    title: 'Create or join a room',
    description: 'Set a topic, difficulty and time limit — or jump into a friend’s room with their code.',
  },
  {
    step: '2',
    title: 'Race the clock',
    description: 'Solve problems in the editor. Every submission is judged instantly against real test cases.',
  },
  {
    step: '3',
    title: 'Climb the leaderboard',
    description: 'Ranks update live as the room submits. Most problems solved, fastest, wins.',
  },
];

const TOPICS = ['Array', 'Dynamic Programming', 'Graphs', 'Trees', 'Binary Search', 'Greedy'];

const MOCK_LEADERBOARD = [
  { rank: 1, name: 'arjun_codes', solved: 4, color: 'text-warning' },
  { rank: 2, name: 'priya.dev', solved: 3, color: 'text-ink-soft' },
  { rank: 3, name: 'you', solved: 3, color: 'text-orange-400', me: true },
];

export default function LandingPage() {
  return (
    <div className="flex flex-col gap-24 py-10">
      <section className="grid items-center gap-12 lg:grid-cols-2">
        <div>
          <Badge tone="primary">
            <Swords size={12} /> Real-time coding battles
          </Badge>

          <h1 className="mt-5 text-4xl font-semibold leading-tight tracking-tight text-ink sm:text-5xl">
            Code head-to-head. <span className="text-primary">Win the room.</span>
          </h1>

          <p className="mt-5 max-w-lg text-base leading-relaxed text-ink-soft">
            Peer Code turns practicing DSA into a live competition. Spin up a room, invite your
            friends, and race to solve problems before the clock runs out.
          </p>

          <div className="mt-8 flex flex-wrap items-center gap-3">
            <Link to="/register">
              <Button className="gap-2 px-5 py-3 text-base">
                Get Started <ArrowRight size={18} />
              </Button>
            </Link>
            <Link to="/login">
              <Button variant="secondary" className="px-5 py-3 text-base">
                Log in
              </Button>
            </Link>
          </div>

          <div className="mt-10 flex flex-wrap gap-2">
            {TOPICS.map((topic) => (
              <Badge key={topic}>{topic}</Badge>
            ))}
          </div>
        </div>

        <Card className="mx-auto w-full max-w-md">
          <div className="mb-4 flex items-center justify-between">
            <div className="flex items-center gap-2 text-sm font-semibold text-ink">
              <Trophy size={16} className="text-warning" /> Room #F3K9A2
            </div>
            <Badge tone="success">Active</Badge>
          </div>

          <div className="mb-4 flex items-center justify-between rounded-lg border border-border bg-surface-2 px-3 py-2 text-sm">
            <span className="text-ink-soft">Time remaining</span>
            <span className="font-mono font-semibold text-ink">04:12</span>
          </div>

          <div className="flex flex-col gap-1">
            {MOCK_LEADERBOARD.map((entry) => (
              <div
                key={entry.rank}
                className={`flex items-center justify-between rounded-lg px-3 py-2 text-sm ${
                  entry.me ? 'bg-primary-soft' : ''
                }`}
              >
                <span className={`flex items-center gap-1.5 font-semibold ${entry.color}`}>
                  <Trophy size={13} />#{entry.rank}
                </span>
                <span className="flex-1 px-3 text-ink">
                  {entry.name}
                  {entry.me && (
                    <span className="ml-2 rounded-full bg-primary-soft px-2 py-0.5 text-xs text-primary">
                      You
                    </span>
                  )}
                </span>
                <span className="text-ink-soft">{entry.solved} solved</span>
              </div>
            ))}
          </div>
        </Card>
      </section>

      <section id="features">
        <div className="mb-10 text-center">
          <h2 className="text-2xl font-semibold text-ink sm:text-3xl">
            Everything you need for a battle
          </h2>
          <p className="mt-2 text-sm text-ink-soft">
            Built for practicing DSA the way it actually gets competitive.
          </p>
        </div>

        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {FEATURES.map(({ icon: Icon, title, description }) => (
            <Card key={title} className="flex flex-col gap-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary-soft text-primary">
                <Icon size={20} />
              </span>
              <h3 className="text-base font-semibold text-ink">{title}</h3>
              <p className="text-sm leading-relaxed text-ink-soft">{description}</p>
            </Card>
          ))}
        </div>
      </section>

      <section id="how-it-works">
        <div className="mb-10 text-center">
          <h2 className="text-2xl font-semibold text-ink sm:text-3xl">How it works</h2>
          <p className="mt-2 text-sm text-ink-soft">Three steps between you and the leaderboard.</p>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          {STEPS.map(({ step, title, description }) => (
            <Card key={step} className="flex flex-col gap-3">
              <span className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-sm font-semibold text-white">
                {step}
              </span>
              <h3 className="text-base font-semibold text-ink">{title}</h3>
              <p className="text-sm leading-relaxed text-ink-soft">{description}</p>
            </Card>
          ))}
        </div>
      </section>

      <section className="rounded-2xl border border-border bg-surface px-6 py-14 text-center sm:px-12">
        <div className="mb-4 flex items-center justify-center gap-2">
          <DifficultyBadge difficulty="easy" />
          <DifficultyBadge difficulty="medium" />
          <DifficultyBadge difficulty="hard" />
        </div>
        <h2 className="text-2xl font-semibold text-ink sm:text-3xl">Ready to battle?</h2>
        <p className="mx-auto mt-2 max-w-md text-sm text-ink-soft">
          Create a free account and have a room running with your friends in under a minute.
        </p>
        <Link to="/register" className="mt-6 inline-block">
          <Button className="gap-2 px-6 py-3 text-base">
            Create your account <ArrowRight size={18} />
          </Button>
        </Link>
      </section>
    </div>
  );
}
