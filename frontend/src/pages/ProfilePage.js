import React, { useState, useEffect } from 'react';
import { updateUserLocation, getUserProfile } from '../services/api';
import { useWeather } from '../context/WeatherContext'; // <-- IMPORT useWeather

function ProfilePage() {
  const [user, setUser] = useState(null);
  const [location, setLocation] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const { refetchWeather } = useWeather(); // <-- GET THE REFETCH FUNCTION

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const profileData = await getUserProfile();
        setUser(profileData);
        setLocation(profileData.location || '');
      } catch (error) {
        setMessage(error.message);
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    try {
      const response = await updateUserLocation(location);
      setMessage(response.message);
      
      // --- THIS IS THE NEW LINE ---
      // After successfully saving, tell the weather system to get new data
      refetchWeather();
      
    } catch (error) {
      setMessage(error.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !user) {
    return <p className="text-center my-5">Loading Profile...</p>;
  }

  if (!user) {
    return <p className="text-center my-5 text-danger">{message || "Could not load user profile."}</p>;
  }

  return (
    <div className="container my-5">
      <div className="row justify-content-center">
        <div className="col-md-8">
          <div className="card shadow-sm border-0">
            <div className="card-header bg-success text-white">
              <h2 className="mb-0">👤 User Profile</h2>
            </div>
            <div className="card-body p-4">
              <div className="mb-4">
                <strong className="d-block text-muted">Username:</strong>
                <span className="fs-5">{user.username}</span>
              </div>
              <div className="mb-4">
                <strong className="d-block text-muted">Email:</strong>
                <span className="fs-5">{user.email}</span>
              </div>
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="location" className="form-label fw-medium">Your Farm's Location (City)</label>
                  <input
                    type="text"
                    id="location"
                    className="form-control"
                    value={location}
                    onChange={(e) => setLocation(e.target.value)}
                    placeholder="e.g., Nashik"
                    required
                  />
                  <div className="form-text">This will be used for personalized weather alerts.</div>
                </div>
                {message && <div className="alert alert-info mt-3">{message}</div>}
                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Saving...' : 'Save Location'}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;