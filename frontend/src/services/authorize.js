import { jwtDecode } from 'jwt-decode';

const TOKEN_KEY = 'authToken';

export const saveToken = (token) => {
  localStorage.setItem(TOKEN_KEY, token);
};

export const getToken = () => {
  return localStorage.getItem(TOKEN_KEY);
};

export const removeToken = () => {
  localStorage.removeItem(TOKEN_KEY);
};

export const isUserLoggedIn = () => {
  const token = getToken();
  if (!token) {
    return false;
  }
  
  try {
    const { exp } = jwtDecode(token);
    if (Date.now() >= exp * 1000) {
      removeToken();
      return false;
    }
  } catch (e) {
    return false;
  }

  return true;
};

// --- THIS IS THE FINAL, UPDATED FUNCTION ---
export const getUser = () => {
  try {
    const token = getToken();
    if (token && isUserLoggedIn()) {
      const decoded = jwtDecode(token);
      // This now correctly reads the user ID from 'sub' and the username/email from the top-level claims
      return { 
          id: decoded.sub,
          username: decoded.username,
          email: decoded.email
      };
    }
    return null;
  } catch (error) {
    console.error('Failed to decode token:', error);
    return null;
  }
};

