import { jwtDecode } from 'jwt-decode';

const TOKEN_KEY = 'authToken';

/**
 * Saves the user's authentication token to localStorage.
 * @param {string} token - The JWT token received from the server.
 */
export const saveToken = (token) => {
  localStorage.setItem(TOKEN_KEY, token);
};

/**
 * Retrieves the authentication token from localStorage.
 * @returns {string|null} The token, or null if it doesn't exist.
 */
export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

/**
 * Removes the authentication token from localStorage (for logout).
 */
export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY);
};

/**
 * Checks if a user is currently logged in by verifying the token.
 * @returns {boolean} True if a valid, unexpired token exists, false otherwise.
 */
export const isUserLoggedIn = () => {
  const token = getToken();
  if (!token) {
    return false;
  }
  
  try {
    const { exp } = jwtDecode(token);
    // Check if the token's expiration time is in the future
    if (Date.now() >= exp * 1000) {
      removeToken(); // Clean up expired token
      return false;
    }
  } catch (e) {
    // If the token is invalid, it will fail to decode
    return false;
  }

  return true;
};

/**
 * Decodes the JWT token to get user information.
 * @returns {object|null} The user payload from the token, or null if no valid token exists.
 */
export const getUser = () => {
  try {
    const token = getToken();
    if (token && isUserLoggedIn()) { // Ensure token is not expired before decoding
      return jwtDecode(token);
    }
    return null;
  } catch (error) {
    console.error('Failed to decode token:', error);
    return null;
  }
};