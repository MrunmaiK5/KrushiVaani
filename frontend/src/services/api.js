import apiClient from './apiClient';
import { getToken } from './authorize';

// --- Auth Functions ---
export const signupUser = async (userData) => {
  try {
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to create account.');
  }
};

export const loginUser = async (credentials) => {
  try {
    const response = await apiClient.post('/auth/login', credentials);
    const { access_token } = response.data;
    if (access_token) {
      localStorage.setItem('authToken', access_token);
    }
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to login.');
  }
};

// --- Profile Functions ---
export const getUserProfile = async () => {
  try {
    const response = await apiClient.get('/auth/profile', {
      headers: { Authorization: `Bearer ${getToken()}` }
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch profile.');
  }
};

export const updateUserLocation = async (location) => {
  try {
    const response = await apiClient.put(
      '/auth/profile/update',
      { location }, // Data to send
      { headers: { Authorization: `Bearer ${getToken()}` } } // Auth header
    );
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to update location.');
  }
};

// --- Recommendation Functions ---
export const getBothRecommendations = async (data) => {
  try {
    const response = await apiClient.post('/recommend/crop-and-fertilizer', data, {
        headers: { Authorization: `Bearer ${getToken()}` }
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch recommendations');
  }
};

export const getFertilizerOnly = async (data) => {
  try {
    const response = await apiClient.post('/recommend/fertilizer-only', data, {
        headers: { Authorization: `Bearer ${getToken()}` }
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch fertilizer plan');
  }
};

