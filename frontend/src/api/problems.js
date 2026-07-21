import api from './axios';

// GET /api/problems/  -> all problems, ordered newest first.
// There is no "get single problem by id" endpoint on the backend, so pages
// that need one problem's full detail (title/description/examples) fetch the
// full list and find it by id client-side.
export function listProblems() {
  return api.get('/problems/');
}
