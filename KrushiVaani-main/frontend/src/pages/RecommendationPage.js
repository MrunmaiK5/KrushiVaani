import React, { useState } from 'react'; // CORRECTED LINE
import { getWeatherData, getBothRecommendations, getFertilizerOnly } from '../services/api';
import RecommendationForm from '../components/RecommendationForm';
import CropResult from '../components/CropResult';
import FertilizerResult from '../components/FertilizerResult';

const RecommendationPage = () => {
  const [formData, setFormData] = useState({ N: '', P: '', K: '', ph: '', location: '', crop: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [cropResult, setCropResult] = useState('');
  const [fertilizerResult, setFertilizerResult] = useState('');

  const handleChange = (e) => {
    setFormData(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setCropResult('');
    setFertilizerResult('');
    try {
      const weatherData = await getWeatherData(formData.location);
      const soilData = { N: formData.N, P: formData.P, K: formData.K, ph: formData.ph };
      const combinedData = { ...soilData, ...weatherData };
      if (formData.crop) {
        const finalData = { ...combinedData, crop: formData.crop };
        const response = await getFertilizerOnly(finalData);
        setFertilizerResult(response.prediction);
      } else {
        const response = await getBothRecommendations(combinedData);
        setCropResult(response.crop_prediction);
        setFertilizerResult(response.fertilizer_prediction);
      }
    } catch (err) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container my-5">
      <div className="row justify-content-center">
        <div className="col-lg-8">
          <div className="card shadow-lg border-0">
            <div className="card-body p-5">
              <h1 className="card-title text-center fw-bold text-dark mb-2">Farm Analysis</h1>
              <p className="card-text text-center text-muted mb-5">
                Enter your soil data and location to get a complete crop and fertilizer plan.
              </p>
              <RecommendationForm
                formData={formData}
                loading={loading}
                handleChange={handleChange}
                handleSubmit={handleSubmit}
              />
              <div className="mt-4">
                {error && <div className="alert alert-danger">{error}</div>}
                <CropResult crop={cropResult} />
                <FertilizerResult fertilizer={fertilizerResult} />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RecommendationPage;