import React from 'react';
import { Link, NavLink } from 'react-router-dom';
// DO NOT import the logo when it's in the public folder

const Navbar = () => {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-success shadow-sm">
      <div className="container">
        <Link className="navbar-brand fw-bold d-flex align-items-center" to="/">
          <img
            src="/images/logo.png" // CORRECTED: Use the direct public path
            alt="KrushiVaani Logo"
            height="40"
            className="me-3"
          />
          KrushiVaani
        </Link>
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarNav">
          <ul className="navbar-nav ms-auto">
            <li className="nav-item">
              <NavLink className="nav-link" aria-current="page" to="/" end>
                Home
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/recommendation">
                Recommendation
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/disease-detection">
                Disease
              </NavLink>
            </li>
             <li className="nav-item">
              <NavLink className="nav-link" to="/weather-alert">
                Weather
              </NavLink>
            </li>
            <li className="nav-item">
              <NavLink className="nav-link" to="/login">
                Login
              </NavLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;