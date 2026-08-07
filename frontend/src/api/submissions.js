import api from './axios';

// POST /api/submissions/submit/  { room: <room DB id>, problem: <problem id>, code, language }
// NOTE: "room" is the Room's database id, not its room_code.
// Judges against the problem's hidden test cases. On a non-accepted verdict,
// the response's `failure_detail` describes the first failing test case.
export function submitSolution({ room, problem, code, language }) {
  return api.post('/submissions/submit/', { room, problem, code, language });
}

// POST /api/submissions/run/  { room: <room DB id>, problem: <problem id>, code, language }
// Runs against only the problem's sample test cases and never creates a
// Submission — for the "Run" / try-before-you-submit workflow. Returns
// { results: [{ input, expected_output, actual_output, passed, verdict, stderr, compile_output }], all_passed }.
export function runSolution({ room, problem, code, language }) {
  return api.post('/submissions/run/', { room, problem, code, language });
}

// GET /api/submissions/history/<room_code>/?mine=true
export function getSubmissionHistory(roomCode, { mine = false } = {}) {
  return api.get(`/submissions/history/${roomCode}/`, {
    params: mine ? { mine: 'true' } : undefined,
  });
}

// GET /api/submissions/<submission_id>/
export function getSubmissionDetail(submissionId) {
  return api.get(`/submissions/${submissionId}/`);
}

// GET /api/submissions/mine/  -> every submission the current user has ever
// made, across all rooms, newest first.
export function getMySubmissions() {
  return api.get('/submissions/mine/');
}
