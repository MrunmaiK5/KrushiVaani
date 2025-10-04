// frontend/src/services/authService.js
import apiClient from './apiClient';

/**
 * Registers a new user.
 * @param {object} userData - {username, email, password}
 * @returns {Promise<object>} The server response.
 */
export const signupUser = async (userData) => {
  try {
    // Correct endpoint: /auth/register
    const response = await apiClient.post('/auth/register', userData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to create account.');
  }
};

/**
 * Logs a user in by sending their credentials to the backend.
 * @param {object} credentials - {email, password}
 * @returns {Promise<string>} The JWT token.
 */
export const loginUser = async (credentials) => {
  try {
    // Correct endpoint: /auth/login
    const response = await apiClient.post('/auth/login', credentials);
    
    const { access_token } = response.data;
    if (access_token) {
      // Save the token to local storage for future requests
      localStorage.setItem('authToken', access_token);
      return access_token;
    }
  } catch (error) {
    throw new Error(error.response?.data?.error || 'Failed to login.');
  }
};