import axios from 'axios';
import { getToken } from './authorize'; // Import your token helper

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Your Flask backend URL
  headers: {
    'Content-Type': 'application/json',
  },
});

// --- ADDED: AXIOS INTERCEPTOR ---
// This ensures that the 'authToken' is automatically included in every request header.
apiClient.interceptors.request.use(
  (config) => {
    const token = getToken(); // Retrieves the token from localStorage
    if (token) {
      // Attaches the Bearer token for Flask-JWT-Extended to validate
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;