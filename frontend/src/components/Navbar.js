import React from 'react';
import { Link, NavLink, useNavigate } from 'react-router-dom';
import { isUserLoggedIn, removeToken } from '../services/authorize';

const Navbar = () => {
  const isAuthenticated = isUserLoggedIn();
  const navigate = useNavigate();

  const handleLogout = () => {
    removeToken(); // Clear the token from storage
    navigate('/login'); // Redirect to the login page
    window.location.reload(); // Force a full refresh to clear all app state
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-success shadow-sm">
      <div className="container">
        <Link className="navbar-brand fw-bold d-flex align-items-center" to="/">
          <img src="/images/logo.png" alt="KrushiVaani Logo" height="40" className="me-3" />
          KrushiVaani
        </Link>
        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <NavLink className="nav-link" to="/" end>Home</NavLink>
            </li>
            {/* Show protected links only if authenticated */}
            {isAuthenticated && (
              <>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/recommendation">Recommendation</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/disease-detection">Disease</NavLink>
                </li>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/weather-alert">Weather</NavLink>
                </li>
              </>
            )}
            
            {isAuthenticated ? (
              <>
                <li className="nav-item">
                  <NavLink className="nav-link" to="/profile">Profile</NavLink>
                </li>
                <li className="nav-item">
                  <button onClick={handleLogout} className="btn btn-link nav-link" style={{ textDecoration: 'none' }}>
                    Logout
                  </button>
                </li>
              </>
            ) : (
              <li className="nav-item">
                <NavLink className="nav-link" to="/login">Login</NavLink>
              </li>
            )}
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;