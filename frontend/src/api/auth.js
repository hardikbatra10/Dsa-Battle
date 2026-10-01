import api from './axios';

// POST /api/users/register/  { username, email, password }
export function registerUser({ username, email, password }) {
  return api.post('/users/register/', { username, email, password });
}

// POST /api/token/  { username, password } -> { access, refresh }
export function login({ username, password }) {
  return api.post('/token/', { username, password });
}

// GET /api/users/me/  -> { email, rating, streak }
export function getMe() {
  return api.get('/users/me/');
}

// GET /api/users/profile/  -> { username, email, rooms_created, problems_solved, total_submissions }
export function getProfile() {
  return api.get('/users/profile/');
}

// POST /api/users/google/  { id_token } -> { access, refresh, created }
// Trades a Firebase Google ID token for this app's own JWT pair.
export function googleLogin(idToken) {
  return api.post('/users/google/', { id_token: idToken });
}

// POST /api/users/username/  { username }
// One-time claim of a real username for a Google-created account.
export function setUsername(username) {
  return api.post('/users/username/', { username });
}
