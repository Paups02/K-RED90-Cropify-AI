import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Document APIs
export const documentsApi = {
  upload: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/api/documents/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  uploadMultiple: async (files) => {
    const formData = new FormData();
    files.forEach((file) => formData.append('files', file));
    const response = await api.post('/api/documents/upload-multiple', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  list: async () => {
    const response = await api.get('/api/documents/');
    return response.data;
  },

  get: async (docId) => {
    const response = await api.get(`/api/documents/${docId}`);
    return response.data;
  },

  delete: async (docId) => {
    const response = await api.delete(`/api/documents/${docId}`);
    return response.data;
  },
};

// Generation APIs
export const generateApi = {
  content: async (params) => {
    const response = await api.post('/api/generate/content', params);
    return response.data;
  },

  query: async (params) => {
    const response = await api.post('/api/generate/query', params);
    return response.data;
  },

  chat: async (params) => {
    const response = await api.post('/api/generate/chat', params);
    return response.data;
  },

  getTypes: async () => {
    const response = await api.get('/api/generate/types');
    return response.data;
  },
};

// Stats API
export const statsApi = {
  get: async () => {
    const response = await api.get('/api/stats');
    return response.data;
  },

  health: async () => {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
