import axios from 'axios';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('access_token');
    const activeOrgId = localStorage.getItem('active_org_id');

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    if (activeOrgId) {
      config.headers['X-Organization-ID'] = activeOrgId;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export default apiClient;