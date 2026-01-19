const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000';

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.message || data.error || 'Request failed');
  return data;
}

export const api = {
  login: (username, password) => request('/login', { method: 'POST', body: JSON.stringify({ username, password }) }),
  register: (username, password) => request('/register', { method: 'POST', body: JSON.stringify({ username, password }) }),
  session: () => request('/api/session'),
  logout: () => request('/api/logout', { method: 'POST' }),
  attendance: () => request('/api/attendance'),
  stats: () => request('/api/stats'),
  analytics: (days = 30) => request(`/api/analytics?days=${days}`),
  startCamera: () => request('/api/start-camera', { method: 'POST' }),
};
