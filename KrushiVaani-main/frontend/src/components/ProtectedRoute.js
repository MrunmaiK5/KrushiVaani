import React from 'react';
import { Navigate } from 'react-router-dom';
import { isUserLoggedIn } from '../services/authorize';

const ProtectedRoute = ({ children }) => {
  const isAuthenticated = isUserLoggedIn();

  if (!isAuthenticated) {
    // If the user is not logged in, redirect them to the login page
    return <Navigate to="/login" replace />;
  }

  // If the user is logged in, show the page they were trying to access
  return children;
};

export default ProtectedRoute;