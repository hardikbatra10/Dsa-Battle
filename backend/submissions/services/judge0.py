import base64
import os
import time

import requests
from dotenv import load_dotenv

from submissions.constants import LANGUAGE_IDS

load_dotenv()

BASE_URL = "https://judge0-ce.p.rapidapi.com"

# Judge0 status ids (https://ce.judge0.com/#statuses-and-languages-status-get):
# 1 In Queue, 2 Processing, 3 Accepted, 4 Wrong Answer (unused here, we
# compute this ourselves), 5 Time Limit Exceeded, 6 Compilation Error,
# 7-14 assorted runtime/internal errors.
STATUS_IN_QUEUE = 1
STATUS_PROCESSING = 2
STATUS_ACCEPTED = 3
STATUS_TIME_LIMIT_EXCEEDED = 5
STATUS_COMPILATION_ERROR = 6
RUNTIME_ERROR_STATUS_IDS = {7, 8, 9, 10, 11, 12, 13, 14}

PENDING_STATUS_IDS = {STATUS_IN_QUEUE, STATUS_PROCESSING}

# Judge0 CE caps a batch at 20 submissions per request.
MAX_BATCH_SIZE = 20

# A batch is submitted once and then polled until every entry has finished.
POLL_INTERVAL_SECONDS = 0.6
POLL_TIMEOUT_SECONDS = 45

# Fields we actually read back, so Judge0 doesn't ship us the whole record.
RESULT_FIELDS = "status,stdout,stderr,compile_output"

# Everything is exchanged base64-encoded, and that is not optional.
#
# With base64_encoded=false, Judge0 refuses to return a batch at all if ANY
# field in it is not valid UTF-8 - it answers the results fetch with
# HTTP 400 "some attributes ... cannot be converted to UTF-8". Compiler
# diagnostics trip this routinely (gcc emits typographic quotes and, on some
# errors, raw bytes), so a single student syntax error would fail the whole
# submission rather than coming back as a compile-error verdict. Programs that
# print arbitrary bytes would do the same.
B64 = "true"


def _encode(text):
    return base64.b64encode((text or "").encode("utf-8")).decode("ascii")


def _decode(value):
    """Decodes one base64 field from Judge0 back to text.

    Lenient on purpose: this is compiler and program output, so it may be
    malformed or not quite UTF-8. Replacing undecodable bytes keeps a usable
    error message instead of raising while reporting someone's error.
    """
    if not value:
        return ""
    try:
        return base64.b64decode(value).decode("utf-8", errors="replace")
    except Exception:
        return ""


class Judge0Error(RuntimeError):
    """Judge0 was unreachable, rejected the request, or never finished."""


def _headers():
    return {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST"),
        "Content-Type": "application/json",
    }


def run_batch(source_code, language, stdins):
    """
    Runs source_code against every stdin in one go and returns the raw Judge0
    result dicts, in the same order as `stdins`.

    Judging used to POST one submission per test case and then redundantly GET
    it back, i.e. two HTTP round trips per case, serially. With a full hidden
    suite that meant ~20 round trips and well over the web server's request
    timeout. Judge0's batch endpoint takes the whole suite in a single POST,
    so a submission now costs one POST plus a handful of polls regardless of
    how many test cases the problem has.
    """
    if not stdins:
        return []

    language_id = LANGUAGE_IDS.get(language)
    if language_id is None:
        raise Judge0Error(f"Judge0 has no language id configured for {language!r}.")

    results = []
    for start in range(0, len(stdins), MAX_BATCH_SIZE):
        chunk = stdins[start:start + MAX_BATCH_SIZE]
        tokens = _submit_batch(source_code, language_id, chunk)
        results.extend(_await_batch(tokens))
    return results


def _submit_batch(source_code, language_id, stdins):
    """Creates one batch of submissions and returns their tokens, in order."""
    payload = {
        "submissions": [
            {
                "source_code": _encode(source_code),
                "language_id": language_id,
                "stdin": _encode(stdin),
            }
            for stdin in stdins
        ]
    }

    try:
        response = requests.post(
            f"{BASE_URL}/submissions/batch?base64_encoded={B64}",
            json=payload,
            headers=_headers(),
            timeout=30,
        )
        response.raise_for_status()
        created = response.json()
    except requests.RequestException as exc:
        raise Judge0Error(f"Could not reach the code execution service: {exc}") from exc
    except ValueError as exc:
        raise Judge0Error("Code execution service returned a malformed response.") from exc

    # A rejected submission comes back as {"error": ...} in place of a token.
    tokens = [entry.get("token") for entry in created]
    if not all(tokens):
        rejected = [entry for entry in created if not entry.get("token")]
        raise Judge0Error(f"Code execution service rejected a submission: {rejected}")

    return tokens


def _await_batch(tokens):
    """Polls a batch until every submission has finished, preserving order."""
    deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
    url = (
        f"{BASE_URL}/submissions/batch"
        f"?tokens={','.join(tokens)}&base64_encoded={B64}&fields={RESULT_FIELDS}"
    )

    while True:
        try:
            response = requests.get(url, headers=_headers(), timeout=30)
            response.raise_for_status()
            submissions = response.json().get("submissions", [])
        except requests.RequestException as exc:
            raise Judge0Error(f"Could not reach the code execution service: {exc}") from exc
        except ValueError as exc:
            raise Judge0Error("Code execution service returned a malformed response.") from exc

        still_running = any(
            (entry.get("status") or {}).get("id") in PENDING_STATUS_IDS
            for entry in submissions
        )
        if not still_running and len(submissions) == len(tokens):
            # status stays as-is (it is an object, never encoded); the three
            # text fields come back base64 and are decoded once, here, so no
            # caller has to know about the encoding.
            for entry in submissions:
                for field in ("stdout", "stderr", "compile_output"):
                    entry[field] = _decode(entry.get(field))
            return submissions

        if time.monotonic() >= deadline:
            raise Judge0Error(
                "Code execution service did not finish in time. Please try again."
            )

        time.sleep(POLL_INTERVAL_SECONDS)


def classify_result(result, testcase):
    """
    Turns one raw Judge0 result into a verdict for `testcase`.

    Always returns the input/expected/actual output (plus stderr and
    compile_output) so callers can show exactly what happened, whether or not
    it passed.
    """
    status_id = (result.get("status") or {}).get("id")
    stdout = (result.get("stdout") or "").strip()
    expected = testcase.expected_output.strip()

    if status_id == STATUS_COMPILATION_ERROR:
        verdict = "compilation_error"
    elif status_id == STATUS_TIME_LIMIT_EXCEEDED:
        verdict = "time_limit_exceeded"
    elif status_id in RUNTIME_ERROR_STATUS_IDS:
        verdict = "runtime_error"
    elif stdout != expected:
        verdict = "wrong_answer"
    else:
        verdict = "accepted"

    return {
        "verdict": verdict,
        "passed": verdict == "accepted",
        "input": testcase.input_data,
        "expected_output": testcase.expected_output,
        "actual_output": stdout,
        "stderr": result.get("stderr") or "",
        "compile_output": result.get("compile_output") or "",
    }


def run_sample_test_cases(problem, source_code, language):
    """
    Used by the "Run" action: executes only the sample (is_sample=True) test
    cases and always reveals input/expected/actual output for each, so the
    user can debug before formally submitting. Never creates a Submission.
    """
    sample_cases = list(problem.test_cases.filter(is_sample=True))
    results = run_batch(source_code, language, [c.input_data for c in sample_cases])
    return [
        classify_result(result, testcase)
        for result, testcase in zip(results, sample_cases)
    ]


def judge_problem(problem, source_code, language):
    """
    Used by "Submit": judges against the hidden (is_sample=False) test cases
    and reports the first one that doesn't pass, so that failure's detail can
    be shown to the user.

    The whole suite is executed in one batch, so the seeded ordering of the
    hidden cases (cheapest and most degenerate first) decides which failure
    gets reported, rather than how much work is done.
    """
    hidden_cases = list(problem.test_cases.filter(is_sample=False))
    results = run_batch(source_code, language, [c.input_data for c in hidden_cases])

    for result, testcase in zip(results, hidden_cases):
        outcome = classify_result(result, testcase)
        if not outcome["passed"]:
            return outcome

    return {
        "verdict": "accepted",
        "passed": True,
        "input": None,
        "expected_output": None,
        "actual_output": None,
        "stderr": "",
        "compile_output": "",
    }
