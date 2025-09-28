import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { signupUser } from '../services/authService';

const SignupPage = () => {
  const [formData, setFormData] = useState({ username: '', email: '', password: '', confirmPassword: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match.');
      return;
    }
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      const { username, email, password } = formData;
      const response = await signupUser({ username, email, password });
      setSuccess('Account created successfully! Redirecting to login...');
      console.log('Signup successful:', response);
      setTimeout(() => navigate('/login'), 2000); // Redirect after 2 seconds
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
              <h1 className="card-title text-center fw-bold text-dark mb-4">Create Account 📝</h1>
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label fw-medium">Username</label>
                  <input type="text" name="username" className="form-control" value={formData.username} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                  <label className="form-label fw-medium">Email address</label>
                  <input type="email" name="email" className="form-control" value={formData.email} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                  <label className="form-label fw-medium">Password</label>
                  <input type="password" name="password" className="form-control" value={formData.password} onChange={handleChange} required />
                </div>
                <div className="mb-3">
                  <label className="form-label fw-medium">Confirm Password</label>
                  <input type="password" name="confirmPassword" className="form-control" value={formData.confirmPassword} onChange={handleChange} required />
                </div>
                {error && <div className="alert alert-danger">{error}</div>}
                {success && <div className="alert alert-success">{success}</div>}
                <div className="d-grid mt-4">
                  <button type="submit" className="btn btn-success" disabled={loading}>
                    {loading ? 'Creating Account...' : 'Sign Up'}
                  </button>
                </div>
              </form>
              <p className="text-center text-muted mt-4">
                Already have an account? <Link to="/login">Login</Link>
              </p>
            </div>
          </div>
        </div>
      </main>
      
    </div>
  );
};

export default SignupPage;