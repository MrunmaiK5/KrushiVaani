import React, { useState, useEffect } from 'react'; // Added useEffect
import { useWeather } from '../context/WeatherContext';
import { getBothRecommendations, getFertilizerOnly, getUserProfile } from '../services/api'; // Added getUserProfile
import RecommendationForm from '../components/RecommendationForm';
import CropResult from '../components/CropResult';
import FertilizerResult from '../components/FertilizerResult';

const RecommendationPage = () => {
  const { weatherData } = useWeather();
  const [formData, setFormData] = useState({ N: '', P: '', K: '', ph: '', location: 'Pune', crop: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [cropResult, setCropResult] = useState('');
  const [fertilizerResult, setFertilizerResult] = useState(null);

  // --- NEW: AUTO-FETCH USER LOCATION ON LOAD ---
  useEffect(() => {
    const fetchUserLocation = async () => {
      try {
        const profile = await getUserProfile(); // Uses the service from your api.js
        if (profile && profile.location) {
          // Set the form's default location to the user's saved farm location
          setFormData(prev => ({ ...prev, location: profile.location }));
        }
      } catch (err) {
        console.error("Profile location fetch failed. Defaulting to Pune.");
      }
    };
    fetchUserLocation();
  }, []); // Runs only once when the page loads

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setCropResult('');
    setFertilizerResult(null);

    try {
      const payload = { 
        N: formData.N, 
        P: formData.P, 
        K: formData.K, 
        ph: formData.ph, 
        location: formData.location,
        temperature: weatherData?.temperature || 25.0,
        humidity: weatherData?.humidity || 70.0,
        rainfall: weatherData?.rainfall || 100.0
      };
      
      if (formData.crop) {
        const response = await getFertilizerOnly({ ...payload, crop: formData.crop });
        setFertilizerResult(response);
      } else {
        const response = await getBothRecommendations(payload);
        setCropResult(response.crop_prediction);
        setFertilizerResult(response.fertilizer_prediction);
      }
    } catch (err) {
      setError(err.message || 'Check if Flask server is running on port 5000');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container my-5">
      {weatherData && (
        <div className="text-end mb-2">
          <small className="text-success fw-bold">
            ● Live Weather Synced: {weatherData.temperature}°C, {weatherData.humidity}% Humidity
          </small>
        </div>
      )}

      <div className="card shadow-lg p-4 p-md-5">
        <h1 className="card-title text-center fw-bold text-dark mb-4">KrushiVaani Farm Advisor</h1>
        
        <RecommendationForm
          formData={formData}
          loading={loading}
          handleChange={handleChange}
          handleSubmit={handleSubmit}
        />

        <div className="mt-4">
          {error && <div className="alert alert-danger">{error}</div>}
          <CropResult crop={cropResult} />
          {fertilizerResult && fertilizerResult.status === "success" && (
            <FertilizerResult 
              fertilizer={fertilizerResult.recommendations.join(' | ')} 
            />
          )}
          {fertilizerResult && fertilizerResult.status === "failed" && (
            <div className="alert alert-warning">
               Logic Error: {fertilizerResult.error}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default RecommendationPage;