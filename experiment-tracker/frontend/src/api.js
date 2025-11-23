import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const experimentsAPI = {
  list: (skip = 0, limit = 20, filters = {}) => {
    const params = new URLSearchParams({ skip, limit });
    if (filters.status) params.append('status', filters.status);
    if (filters.user) params.append('user', filters.user);
    return api.get(`/experiments?${params}`);
  },

  get: (id) => api.get(`/experiments/${id}`),

  create: (data) => api.post('/experiments', data),

  update: (id, data) => api.patch(`/experiments/${id}`, data),

  delete: (id) => api.delete(`/experiments/${id}`),

  compare: (experimentIds) => 
    api.post('/experiments/compare', { experiment_ids: experimentIds }),
};