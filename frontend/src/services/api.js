import apiClient from './apiClient';
import { getToken } from './authorize';

// --- Auth & User Profile Functions ---
// Blueprints: user_bp is registered with url_prefix='/auth'

export const signupUser = async (userData) => {
  try {
    // UPDATED: Matches @user_bp.route('/register') with '/auth' prefix
    const response = await apiClient.post('/auth/register', userData); 
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to create account.');
  }
};

export const loginUser = async (credentials) => {
  try {
    // UPDATED: Matches @user_bp.route('/login') with '/auth' prefix
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

export const getUserProfile = async () => {
  try {
    // UPDATED: Matches @user_bp.route('/profile') with '/auth' prefix
    // CRITICAL: Fixes the "Failed to fetch profile" error on RecommendationPage
    const response = await apiClient.get('/auth/profile'); 
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to fetch profile.');
  }
};

export const updateUserLocation = async (location) => {
  try {
    // UPDATED: Matches @user_bp.route('/profile/update') with '/auth' prefix
    const response = await apiClient.put('/auth/profile/update', { location });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to update location.');
  }
};

// --- Recommendation Functions ---
// Blueprints: recommendation_bp is registered with url_prefix='/recommend'

export const getBothRecommendations = async (data) => {
  try {
    // Payload includes: N, P, K, ph, location. Backend merges Weather data.
    const response = await apiClient.post('/recommend/both', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to fetch hybrid recommendations');
  }
};

export const getFertilizerOnly = async (data) => {
  try {
    const response = await apiClient.post('/recommend/fertilizer', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.message || 'Failed to fetch fertilizer plan');
  }
};

// --- Disease Detection Functions ---
export const detectDisease = async (imageFile) => {
  try {
    const formData = new FormData();
    formData.append('file', imageFile);
    // Note: Verify your disease blueprint prefix (e.g., /disease)
    const response = await apiClient.post('/disease/predict', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to analyze leaf image.');
  }
};