"""Seeds/repairs the Problem + TestCase catalog so every topic x difficulty
combination has at least one usable problem, and every problem has both
sample (is_sample=True) and hidden (is_sample=False) test cases.

Expected outputs are never typed in by hand: each problem defines a small
Python reference solution, and this command actually executes it against
each raw input to compute the correct expected_output. That's the only way
to be confident the seeded test data is right.

Safe to re-run: existing problems are matched by title and only the fields
this command owns are updated; test cases for a problem are fully replaced
each run so there's never stale/duplicate data.

About hidden_inputs: these are the suite a solution is judged against on
Submit, so each one is chosen to break a specific wrong-but-plausible
implementation rather than to add bulk - degenerate sizes, single-element
inputs, all-equal values, negatives and zero, both monotonic directions,
answers pinned at the first and last position, and numeric limits.

Two ordering rules matter:
  * cases are listed cheapest and most degenerate first. The suite runs as a
    single Judge0 batch, so this does not change how much work is done - it
    decides which failure judge_problem() reports, and a minimal failing case
    is far easier to debug than a large one.
  * a sample input is never repeated here. Samples are already visible and
    are re-run by the Run action, so judging one again on Submit spends
    another Judge0 submission for no extra signal.

The problems themselves live in problems/catalog/, one module per
topic. This file only owns how they are written to the database.
"""

import time

from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db.utils import InterfaceError, OperationalError

from problems.catalog import PROBLEMS
from problems.models import Problem, TestCase
from users.models import User

# The hosted Postgres sits behind a connection pooler that will close an
# idle or long-lived connection out from under a run this size. That is a
# transport failure, not a data problem, so the fix is to reconnect and
# retry the one problem that was in flight rather than abandon the run.
RECONNECT_ATTEMPTS = 5


class Command(BaseCommand):
    help = "Seeds/repairs problems and their sample + hidden test cases."

    def add_arguments(self, parser):
        parser.add_argument(
            "--only",
            help="Seed just one topic, e.g. --only graphs.",
        )

    def handle(self, *args, **options):
        owner = User.objects.filter(is_superuser=True).order_by("id").first()
        if owner is None:
            self.stderr.write(self.style.ERROR(
                "No superuser exists to own seeded problems. Create one first: "
                "python manage.py createsuperuser"
            ))
            return

        specs = PROBLEMS
        if options.get("only"):
            specs = [p for p in PROBLEMS if p["topic"] == options["only"]]
            if not specs:
                self.stderr.write(self.style.ERROR(
                    f"No problems with topic {options['only']!r}."
                ))
                return

        written = 0
        try:
            for spec in specs:
                # One transaction PER PROBLEM, not one around the whole run.
                #
                # A single transaction over the entire catalog grew long enough
                # that the hosted Postgres connection dropped mid-run, rolling
                # everything back and never completing. Per-problem scope keeps
                # each transaction short while preserving the property that
                # actually matters: a problem's test cases are replaced all at
                # once, so no problem is ever left holding a partial suite.
                #
                # If the connection does drop, problems already committed stay
                # committed and re-running finishes the job, because
                # update_or_create matches on title and is idempotent.
                self._seed_with_retry(spec, owner)
                written += 1
        except Exception as exc:
            self.stderr.write(self.style.ERROR(
                f"Failed after {written} of {len(specs)} problems: {exc}"
            ))
            self.stderr.write(self.style.WARNING(
                "Problems already written are committed. Re-run to finish - "
                "the command is idempotent."
            ))
            raise

        self.stdout.write(self.style.SUCCESS(f"Done. {written} problems seeded."))

    def _seed_with_retry(self, spec, owner):
        """Seeds one problem, reconnecting if the pooler drops the socket.

        Only connection-level errors are retried. Anything else - a bad
        reference solution, a constraint violation - is a real defect and
        is re-raised immediately so it is not silently papered over.
        """
        for attempt in range(1, RECONNECT_ATTEMPTS + 1):
            try:
                with transaction.atomic():
                    self._seed_one(spec, owner)
                return
            except (OperationalError, InterfaceError) as exc:
                if attempt == RECONNECT_ATTEMPTS:
                    raise
                self.stderr.write(self.style.WARNING(
                    f"Connection lost on {spec['title']!r} "
                    f"(attempt {attempt}/{RECONNECT_ATTEMPTS}): {exc}. "
                    f"Reconnecting."
                ))
                # Drop the dead socket so the next query opens a fresh one.
                connection.close()
                time.sleep(2 * attempt)

    def _seed_one(self, spec, owner):
        solve = spec["solve"]
        example_output = solve(spec["example_input"].split("\n"))

        problem, _ = Problem.objects.update_or_create(
            title=spec["title"],
            defaults={
                "topic": spec["topic"],
                "difficulty": spec["difficulty"],
                "description": spec["description"],
                "example_input": spec["example_input"],
                "example_output": example_output,
                "constraints": spec["constraints"],
                "created_by": owner,
            },
        )

        problem.test_cases.all().delete()

        test_cases = []
        for raw_input in spec["sample_inputs"]:
            test_cases.append(TestCase(
                problem=problem,
                input_data=raw_input,
                expected_output=solve(raw_input.split("\n")),
                is_sample=True,
            ))
        for raw_input in spec["hidden_inputs"]:
            test_cases.append(TestCase(
                problem=problem,
                input_data=raw_input,
                expected_output=solve(raw_input.split("\n")),
                is_sample=False,
            ))
        TestCase.objects.bulk_create(test_cases)

        self.stdout.write(self.style.SUCCESS(
            f"{problem.title} ({problem.topic}/{problem.difficulty}): "
            f"{len(spec['sample_inputs'])} sample + "
            f"{len(spec['hidden_inputs'])} hidden test cases"
        ))
