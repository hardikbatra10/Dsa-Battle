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
