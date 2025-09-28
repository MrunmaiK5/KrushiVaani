import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { loginUser } from '../services/authService';

const LoginPage = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await loginUser(formData);
      // Assuming the backend returns a token, you would save it here
      // For example: localStorage.setItem('token', response.token);
      console.log('Login successful:', response);
      navigate('/'); // Redirect to homepage on successful login
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex flex-column min-vh-100">
      
      <main className="container flex-grow-1 d-flex justify-content-center align-items-center my-5">
        <div className="col-md-6 col-lg-5">
          <div className="card shadow-lg border-0">
            <div className="card-body p-5">
              <h1 className="card-title text-center fw-bold text-dark mb-4">Login 👤</h1>
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="emailInput" className="form-label fw-medium">Email address</label>
                  <input type="email" name="email" className="form-control" id="emailInput" value={formData.email} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                  <label htmlFor="passwordInput" className="form-label fw-medium">Password</label>
                  <input type="password" name="password" className="form-control" id="passwordInput" value={formData.password} onChange={handleChange} required />
                </div>
                {error && <div className="alert alert-danger">{error}</div>}
                <div className="d-grid mt-4">
                  <button type="submit" className="btn btn-success" disabled={loading}>
                    {loading ? 'Logging in...' : 'Login'}
                  </button>
                </div>
              </form>
              <p className="text-center text-muted mt-4">
                Don't have an account? <Link to="/signup">Sign Up</Link>
              </p>
            </div>
          </div>
        </div>
      </main>
    
    </div>
  );
};

export default LoginPage;

