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
export function startRoom(roomCode) {
  return api.post(`/rooms/${roomCode}/start/`);
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
