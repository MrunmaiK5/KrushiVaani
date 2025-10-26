import React from 'react';

const RecommendationForm = ({ formData, loading, handleChange, handleSubmit }) => {
  const cropTypes = ['rice','maize','chickpea','kidneybeans','pigeonpeas','mothbeans','mungbean','blackgram','lentil','pomegranate',
  'banana','mango','grapes','watermelon','muskmelon','apple','orange','papaya','coconut','cotton','jute','coffee'];

  return (
    <form onSubmit={handleSubmit}>
      <div className="row g-4">
        <div className="col-md-6"><InputField label="Nitrogen (N)" name="N" value={formData.N} onChange={handleChange} placeholder="e.g., 90" /></div>
        <div className="col-md-6"><InputField label="Phosphorous (P)" name="P" value={formData.P} onChange={handleChange} placeholder="e.g., 42" /></div>
        <div className="col-md-6"><InputField label="Potassium (K)" name="K" value={formData.K} onChange={handleChange} placeholder="e.g., 43" /></div>
        <div className="col-md-6"><InputField label="pH Value" name="ph" value={formData.ph} onChange={handleChange} placeholder="e.g., 6.5" /></div>
        <div className="col-md-6">
            <label htmlFor="location" className="form-label fw-medium">Location</label>
            <input type="text" id="location" name="location" value={formData.location} onChange={handleChange} className="form-control" placeholder="Enter city or village" required />
        </div>
        <div className="col-md-6">
            <label htmlFor="crop" className="form-label fw-medium">Select Crop (Optional)</label>
            <select id="crop" name="crop" value={formData.crop} onChange={handleChange} className="form-select">
                <option value="">Predict Best Crop For Me</option>
                {cropTypes.map(c => <option key={c} value={c}>{c}</option>)}
            </select>
        </div>
      </div>
      <div className="d-grid mt-5">
        <button type="submit" disabled={loading} className="btn btn-success btn-lg">
          {loading ? 'Analyzing...' : 'Get Recommendation'}
        </button>
      </div>
    </form>
  );
};
const InputField = ({ label, name, value, onChange, placeholder }) => (
  <div>
    <label htmlFor={name} className="form-label fw-medium">{label}</label>
    <input type="number" id={name} name={name} value={value} onChange={onChange} placeholder={placeholder} step="any" required className="form-control" />
  </div>
);
export default RecommendationForm;