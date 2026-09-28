import api from './axios';

// POST /api/rooms/create/  { topic, difficulty, number_of_questions, time_limit_minutes }
export function createRoom({ topic, difficulty, number_of_questions, time_limit_minutes }) {
  return api.post('/rooms/create/', {
    topic,
    difficulty,
    number_of_questions,
    time_limit_minutes,
  });
}

// POST /api/rooms/join/  { room_code }
export function joinRoom(roomCode) {
  return api.post('/rooms/join/', { room_code: roomCode });
}

// GET /api/rooms/<room_code>/
export function getRoom(roomCode) {
  return api.get(`/rooms/${roomCode}/`);
}

// POST /api/rooms/<room_code>/start/
// Returns 409 with { joined, can_force } when the creator is alone in the
// room; re-send with force=true to start anyway.
export function startRoom(roomCode, { force = false } = {}) {
  return api.post(`/rooms/${roomCode}/start/`, force ? { force: true } : {});
}

// POST /api/rooms/<room_code>/end/
export function endRoom(roomCode) {
  return api.post(`/rooms/${roomCode}/end/`);
}

// POST /api/rooms/<room_code>/leave/
export function leaveRoom(roomCode) {
  return api.post(`/rooms/${roomCode}/leave/`);
}

// GET /api/rooms/<room_code>/leaderboard/  -> [{ username, solved, attempts, rank }]
export function getLeaderboard(roomCode) {
  return api.get(`/rooms/${roomCode}/leaderboard/`);
}

// GET /api/rooms/mine/  -> rooms the current user created or joined, newest first
export function getMyRooms() {
  return api.get('/rooms/mine/');
}
