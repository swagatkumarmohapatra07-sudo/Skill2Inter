// API base URL — uses Vite proxy in dev, direct URL in production
const BASE_URL = import.meta.env.VITE_API_URL || '/api';

const api = {
  async get(path) {
    const res = await fetch(`${BASE_URL}${path}`);
    if (!res.ok) throw new Error((await res.json()).detail || `HTTP ${res.status}`);
    return res.json();
  },

  async post(path, body) {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error((await res.json()).detail || `HTTP ${res.status}`);
    return res.json();
  },

  async put(path, body) {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error((await res.json()).detail || `HTTP ${res.status}`);
    return res.json();
  },

  async delete(path) {
    const res = await fetch(`${BASE_URL}${path}`, { method: 'DELETE' });
    if (!res.ok && res.status !== 204) throw new Error(`HTTP ${res.status}`);
  },

  async upload(path, formData) {
    const res = await fetch(`${BASE_URL}${path}`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error((await res.json()).detail || `HTTP ${res.status}`);
    return res.json();
  },
};

// ── Student endpoints ────────────────────────────────────────────────────────
export const studentAPI = {
  login: (email, password) => api.post('/students/login', { email, password }),
  create: (data) => api.post('/students/', data),
  get: (id) => api.get(`/students/${id}`),
  list: () => api.get('/students/'),
  update: (id, data) => api.put(`/students/${id}`, data),
  addSkill: (id, skill) => api.post(`/students/${id}/skills`, skill),
  removeSkill: (sid, skid) => api.delete(`/students/${sid}/skills/${skid}`),
  replaceSkills: (id, skills) => api.put(`/students/${id}/skills`, skills),
  addProject: (id, project) => api.post(`/students/${id}/projects`, project),
  removeProject: (sid, pid) => api.delete(`/students/${sid}/projects/${pid}`),
  addExperience: (id, exp) => api.post(`/students/${id}/experiences`, exp),
  addCertification: (id, cert) => api.post(`/students/${id}/certifications`, cert),
};

// ── Internship endpoints ─────────────────────────────────────────────────────
export const internshipAPI = {
  list: (params = {}) => {
    const q = new URLSearchParams(params).toString();
    return api.get(`/internships/${q ? '?' + q : ''}`);
  },
  get: (id) => api.get(`/internships/${id}`),
  create: (data) => api.post('/internships/', data),
  update: (id, data) => api.put(`/internships/${id}`, data),
  delete: (id) => api.delete(`/internships/${id}`),
  analyzeDescription: (description) => api.post('/internships/analyze', { description }),
};

// ── Match endpoints ──────────────────────────────────────────────────────────
export const matchAPI = {
  calculate: (student_id, internship_id) =>
    api.post('/match/', { student_id, internship_id }),
  get: (match_id) => api.get(`/match/${match_id}`),
  getByStudent: (student_id) => api.get(`/match/student/${student_id}`),
  whatIf: (student_id, internship_id, hypothetical_skills) =>
    api.post('/match/what-if', { student_id, internship_id, hypothetical_skills }),
  compare: (student_id, internship_ids) =>
    api.post('/match/compare', { student_id, internship_ids }),
};

// ── Recommendations + Dashboard ──────────────────────────────────────────────
export const recommendationAPI = {
  get: (student_id, limit = 12) =>
    api.get(`/recommendations/${student_id}?limit=${limit}`),
};

export const dashboardAPI = {
  get: (student_id) => api.get(`/dashboard/${student_id}`),
};

// ── Resume ───────────────────────────────────────────────────────────────────
export const resumeAPI = {
  analyze: (file) => {
    const form = new FormData();
    form.append('file', file);
    return api.upload('/resume/analyze', form);
  },
};

export default api;
