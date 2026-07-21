import os
import requests
from dotenv import load_dotenv
from submissions.constants import LANGUAGE_IDS

load_dotenv()

# Judge0 status ids (https://ce.judge0.com/#statuses-and-languages-status-get):
# 1 In Queue, 2 Processing, 3 Accepted, 4 Wrong Answer (unused here, we
# compute this ourselves), 5 Time Limit Exceeded, 6 Compilation Error,
# 7-14 assorted runtime/internal errors.
STATUS_ACCEPTED = 3
STATUS_TIME_LIMIT_EXCEEDED = 5
STATUS_COMPILATION_ERROR = 6
RUNTIME_ERROR_STATUS_IDS = {7, 8, 9, 10, 11, 12, 13, 14}


def test_judge0_connection():

    url = "https://judge0-ce.p.rapidapi.com/languages"

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST")
    }

    response = requests.get(
        url,
        headers=headers
    )

def run_code(source_code, language, stdin):

    url = "https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=false&wait=true"

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": os.getenv("RAPIDAPI_HOST"),
        "Content-Type": "application/json"
    }
    payload = {
        "source_code" : source_code,
        "language_id" : LANGUAGE_IDS[language],
        "stdin": stdin
    }

    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    token = response.json()["token"]

    result_url = (
        f"https://judge0-ce.p.rapidapi.com/submissions/{token}"
        "?base64_encoded=false"
    )
    result = requests.get(
        result_url,
        headers=headers
    )
    result_json = result.json()
    return result_json


def run_single_test_case(source_code, language, testcase):
    """
    Executes source_code against one TestCase and classifies the outcome.
    Always returns the input/expected/actual output (plus stderr/compile_output)
    so callers can show exactly what happened, whether or not it passed.
    """
    result = run_code(source_code, language, testcase.input_data)

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
    sample_cases = problem.test_cases.filter(is_sample=True)
    return [
        run_single_test_case(source_code, language, testcase)
        for testcase in sample_cases
    ]


def judge_problem(problem, source_code, language):
    """
    Used by "Submit": judges against the hidden (is_sample=False) test cases
    and stops at the first one that doesn't pass, so that failure's detail
    can be shown to the user.
    """
    hidden_cases = problem.test_cases.filter(is_sample=False)

    for testcase in hidden_cases:
        outcome = run_single_test_case(source_code, language, testcase)
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
