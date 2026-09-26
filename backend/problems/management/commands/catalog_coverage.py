"""Reports how far the problem catalog is from its target shape.

The goal is 500 problems - 150 easy, 200 medium, 150 hard - spread as evenly
as the topics allow. This command does not touch the database: it reads
problems/catalog/ directly, so it answers "what is left to write", not "what
is seeded".

Allocation uses water-filling rather than a flat divide. A flat 150/15 = 10
would demand removing problems from cells that already sit above their share
(sliding_window/medium, say). Instead every existing problem is kept and the
remaining budget is handed out one at a time to whichever topic is currently
lowest, which levels the catalog up without ever asking for a negative.
"""

from django.core.management.base import BaseCommand

from problems.catalog import PROBLEMS
from problems.models import Problem


GOALS = {"easy": 150, "medium": 200, "hard": 150}
DIFFICULTIES = ["easy", "medium", "hard"]


def plan(current_by_topic, goal):
    """Level topics up to `goal` total, never reducing an existing count."""
    targets = dict(current_by_topic)
    budget = goal - sum(targets.values())
    if budget < 0:
        return targets, budget            # already over goal, nothing to add
    for _ in range(budget):
        lowest = min(targets, key=lambda t: (targets[t], t))
        targets[lowest] += 1
    return targets, 0


class Command(BaseCommand):
    help = "Shows catalog coverage against the 150/200/150 target."

    def add_arguments(self, parser):
        parser.add_argument(
            "--seeded",
            action="store_true",
            help="Count rows in the database instead of the catalog source.",
        )

    def handle(self, *args, **options):
        if options["seeded"]:
            rows = list(Problem.objects.values_list("topic", "difficulty"))
            source = "database"
        else:
            rows = [(p["topic"], p["difficulty"]) for p in PROBLEMS]
            source = "problems/catalog/"

        topics = sorted({t for t, _ in rows})
        counts = {(t, d): 0 for t in topics for d in DIFFICULTIES}
        for t, d in rows:
            counts[(t, d)] += 1

        targets = {}
        overage = {}
        for d in DIFFICULTIES:
            current = {t: counts[(t, d)] for t in topics}
            tgt, over = plan(current, GOALS[d])
            overage[d] = over
            for t in topics:
                targets[(t, d)] = tgt[t]

        self.stdout.write(f"source: {source}   problems: {len(rows)}\n")
        header = f"{'topic':<18}" + "".join(f"{d:>18}" for d in DIFFICULTIES) + f"{'left':>7}"
        self.stdout.write(header)
        self.stdout.write("-" * len(header))

        total_left = 0
        for t in topics:
            line = f"{t:<18}"
            row_left = 0
            for d in DIFFICULTIES:
                have, want = counts[(t, d)], targets[(t, d)]
                need = max(0, want - have)
                row_left += need
                cell = f"{have}/{want}" + (f" +{need}" if need else " ok")
                line += f"{cell:>18}"
            total_left += row_left
            self.stdout.write(line + f"{row_left:>7}")

        self.stdout.write("-" * len(header))
        totals = f"{'TOTAL':<18}"
        for d in DIFFICULTIES:
            have = sum(counts[(t, d)] for t in topics)
            totals += f"{str(have) + '/' + str(GOALS[d]):>18}"
        self.stdout.write(totals + f"{total_left:>7}")

        self.stdout.write("")
        for d in DIFFICULTIES:
            if overage[d] < 0:
                self.stdout.write(self.style.WARNING(
                    f"{d}: already {-overage[d]} over the {GOALS[d]} goal"
                ))

        if total_left:
            self.stdout.write(self.style.WARNING(
                f"{total_left} problems still to write "
                f"({total_left / 22:.0f} batches at ~22 each)"
            ))
        else:
            self.stdout.write(self.style.SUCCESS("catalog is complete"))
