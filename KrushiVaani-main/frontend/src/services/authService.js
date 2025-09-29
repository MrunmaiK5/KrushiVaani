import apiClient from './apiClient'; // CORRECTED: Import the Axios instance

/**
 * Logs a user in by sending their credentials to the backend.
 * @param {object} credentials - {email, password}
 * @returns {Promise<object>} The server response, likely containing a token.
 */
export const loginUser = async (credentials) => {
  try {
    const response = await apiClient.post('/api/users/login', credentials);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to login.');
  }
};

/**
 * Registers a new user.
 * @param {object} userData - {username, email, password}
 * @returns {Promise<object>} The server response.
 */
export const signupUser = async (userData) => {
  try {
    const response = await apiClient.post('/api/users/register', userData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to create account.');
  }
};