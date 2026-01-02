// import React from 'react';

// const RecommendationForm = ({ formData, loading, handleChange, handleSubmit }) => {
//   const cropTypes = ['rice','maize','chickpea','kidneybeans','pigeonpeas','mothbeans','mungbean','blackgram','lentil','pomegranate',
//   'banana','mango','grapes','watermelon','muskmelon','apple','orange','papaya','coconut','cotton','jute','coffee'];

//   return (
//     <form onSubmit={handleSubmit}>
//       <div className="row g-4">
//         <div className="col-md-6"><InputField label="Nitrogen (N)" name="N" value={formData.N} onChange={handleChange} placeholder="e.g., 90" /></div>
//         <div className="col-md-6"><InputField label="Phosphorous (P)" name="P" value={formData.P} onChange={handleChange} placeholder="e.g., 42" /></div>
//         <div className="col-md-6"><InputField label="Potassium (K)" name="K" value={formData.K} onChange={handleChange} placeholder="e.g., 43" /></div>
//         <div className="col-md-6"><InputField label="pH Value" name="ph" value={formData.ph} onChange={handleChange} placeholder="e.g., 6.5" /></div>
//         <div className="col-md-6">
//             <label htmlFor="location" className="form-label fw-medium">Location</label>
//             <input type="text" id="location" name="location" value={formData.location} onChange={handleChange} className="form-control" placeholder="Enter city or village" required />
//         </div>
//         <div className="col-md-6">
//             <label htmlFor="crop" className="form-label fw-medium">Select Crop (Optional)</label>
//             <select id="crop" name="crop" value={formData.crop} onChange={handleChange} className="form-select">
//                 <option value="">Predict Best Crop For Me</option>
//                 {cropTypes.map(c => <option key={c} value={c}>{c}</option>)}
//             </select>
//         </div>
//       </div>
//       <div className="d-grid mt-5">
//         <button type="submit" disabled={loading} className="btn btn-success btn-lg">
//           {loading ? 'Analyzing...' : 'Get Recommendation'}
//         </button>
//       </div>
//     </form>
//   );
// };
// const InputField = ({ label, name, value, onChange, placeholder }) => (
//   <div>
//     <label htmlFor={name} className="form-label fw-medium">{label}</label>
//     <input type="number" id={name} name={name} value={value} onChange={onChange} placeholder={placeholder} step="any" required className="form-control" />
//   </div>
// );
// export default RecommendationForm;

import React from 'react';
import VoiceButton from './VoiceButton'; // Import the new dual-mode button

const RecommendationForm = ({ formData, loading, handleChange, handleSubmit, setFormData }) => {
  const cropTypes = ['rice','maize','chickpea','kidneybeans','pigeonpeas','mothbeans','mungbean','blackgram','lentil','pomegranate',
  'banana','mango','grapes','watermelon','muskmelon','apple','orange','papaya','coconut','cotton','jute','coffee'];

  // Helper to extract numbers from voice input and update form
  const handleVoiceInput = (name, voiceText) => {
    // Basic regex to find digits in the speech string
    const match = voiceText.match(/\d+/);
    if (match && setFormData) {
      const simulatedEvent = {
        target: { name, value: match[0] }
      };
      handleChange(simulatedEvent);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="shadow-lg p-4 rounded bg-white">
      <div className="row g-4">
        {/* N, P, K with Voice Input Icons */}
        <div className="col-md-4">
          <div className="d-flex align-items-end gap-2">
            <div className="flex-grow-1">
              <InputField label="Nitrogen (N)" name="N" value={formData.N} onChange={handleChange} placeholder="e.g., 90" />
            </div>
            <VoiceButton onSpeechResult={(text) => handleVoiceInput("N", text)} />
          </div>
        </div>

        <div className="col-md-4">
          <div className="d-flex align-items-end gap-2">
            <div className="flex-grow-1">
              <InputField label="Phosphorous (P)" name="P" value={formData.P} onChange={handleChange} placeholder="e.g., 42" />
            </div>
            <VoiceButton onSpeechResult={(text) => handleVoiceInput("P", text)} />
          </div>
        </div>

        <div className="col-md-4">
          <div className="d-flex align-items-end gap-2">
            <div className="flex-grow-1">
              <InputField label="Potassium (K)" name="K" value={formData.K} onChange={handleChange} placeholder="e.g., 43" />
            </div>
            <VoiceButton onSpeechResult={(text) => handleVoiceInput("K", text)} />
          </div>
        </div>

        <div className="col-md-6">
          <InputField label="pH Value" name="ph" value={formData.ph} onChange={handleChange} placeholder="e.g., 6.5" />
        </div>

        <div className="col-md-6">
          <label htmlFor="location" className="form-label fw-medium text-dark">Location / Thikan</label>
          <input type="text" id="location" name="location" value={formData.location} onChange={handleChange} className="form-control form-control-lg" placeholder="Enter city or village" required />
        </div>

        <div className="col-md-12">
          <label htmlFor="crop" className="form-label fw-medium text-dark">Select Crop (Optional)</label>
          <select id="crop" name="crop" value={formData.crop} onChange={handleChange} className="form-select form-select-lg border-success">
            <option value="">Predict Best Crop For Me (AI Recommendation)</option>
            {cropTypes.map(c => <option key={c} value={c}>{c.toUpperCase()}</option>)}
          </select>
          <small className="text-success mt-1 d-block">Tip: Leave empty if you want our Random Forest model to decide.</small>
        </div>
      </div>

      <div className="d-grid mt-5">
        <button type="submit" disabled={loading} className={`btn btn-lg ${loading ? 'btn-secondary' : 'btn-success shadow-sm'}`}>
          {loading ? (
            <div className="d-flex align-items-center justify-content-center gap-2">
              <span className="spinner-border spinner-border-sm" role="status"></span>
              <span>AI is Analyzing Soil...</span>
            </div>
          ) : 'Get Recommendation / Salla Milva'}
        </button>
      </div>
    </form>
  );
};

const InputField = ({ label, name, value, onChange, placeholder }) => (
  <div className="w-100">
    <label htmlFor={name} className="form-label fw-medium text-dark">{label}</label>
    <input 
      type="number" 
      id={name} 
      name={name} 
      value={value} 
      onChange={onChange} 
      placeholder={placeholder} 
      step="any" 
      required 
      className="form-control form-control-lg shadow-sm" 
    />
  </div>
);

export default RecommendationForm;