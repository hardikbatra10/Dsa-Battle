import os
import requests
from dotenv import load_dotenv
from submissions.constants import LANGUAGE_IDS

load_dotenv()


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

    url = "https://judge0-ce.p.rapidapi.com/submissions?base64_encoded=false&wait=false"

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
    
    print(response.status_code)
    token = response.json()["token"]
    print(token)

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

def judge_problem(problem, source_code, language):

    test_cases = problem.test_cases.all()

    for testcase in test_cases:

        result = run_code(
            source_code,
            language,
            testcase.input_data
        )

        stdout = result["stdout"] or ""
        expected = testcase.expected_output

        if stdout.strip() != expected.strip():
            return "wrong_answer"

    return "accepted"