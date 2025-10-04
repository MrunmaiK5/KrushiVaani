import React, { useState } from 'react';
import { getBothRecommendations, getFertilizerOnly } from '../services/api';
import RecommendationForm from '../components/RecommendationForm';
import CropResult from '../components/CropResult';
import FertilizerResult from '../components/FertilizerResult';

const RecommendationPage = () => {
  const [formData, setFormData] = useState({ N: '', P: '', K: '', ph: '', location: 'Pune', crop: '' });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [cropResult, setCropResult] = useState('');
  const [fertilizerResult, setFertilizerResult] = useState(null);

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
      const soilData = { N: formData.N, P: formData.P, K: formData.K, ph: formData.ph, location: formData.location };
      
      if (formData.crop) {
        const finalData = { ...soilData, crop: formData.crop };
        const response = await getFertilizerOnly(finalData);
        setFertilizerResult(response.prediction);
      } else {
        const response = await getBothRecommendations(soilData);
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
      <div className="card shadow-lg p-4 p-md-5">
        <h1 className="card-title text-center fw-bold text-dark mb-4">Farm Analysis Advisor</h1>
        <RecommendationForm
          formData={formData}
          loading={loading}
          handleChange={handleChange}
          handleSubmit={handleSubmit}
        />
        <div className="mt-4">
          {error && <div className="alert alert-danger">{error}</div>}
          <CropResult crop={cropResult} />
          {fertilizerResult && <FertilizerResult fertilizer={fertilizerResult.recommended_fertilizers.join(', ')} />}
        </div>
      </div>
    </div>
  );
};

export default RecommendationPage;