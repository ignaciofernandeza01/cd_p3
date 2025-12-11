import api from './axios'; // tu axios con baseURL + token

export function listGames(q = '') {
  const params = q ? { q } : {};
  return api.get('/games', { params }).then(r => r.data);
}

export function getGame(id) {
  return api.get(`/games/${id}`).then(r => r.data);
}

export function createGame(payload) {
  return api.post('/games', payload).then(r => r.data);
}

export function updateGame(id, payload) {
  return api.patch(`/games/${id}`, payload).then(r => r.data);
}

export function deleteGame(id) {
  return api.delete(`/games/${id}`);
}
