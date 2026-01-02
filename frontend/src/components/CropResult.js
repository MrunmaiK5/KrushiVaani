// // src/components/CropResult.js
// import React from 'react';
// const CropResult = ({ crop }) => {
//   if (!crop) return null;
//   return (
//     <div className="alert alert-success border-success mt-4">
//       <h2 className="alert-heading h4 fw-bold">Recommended Crop: 🌾</h2>
//       <p className="mb-0 fs-5 text-capitalize">{crop}</p>
//     </div>
//   );
// };
// export default CropResult;

import React from 'react';
import VoiceButton from './VoiceButton'; // Import our new shared component
import { Sprout, CheckCircle } from 'lucide-react';

const CropResult = ({ crop }) => {
  if (!crop) return null;

  // The script the AI will read out loud to the farmer
  const voiceScript = `Congratulations! Based on your soil analysis, the most recommended crop for your land is ${crop}. This crop has the highest success rate for your current Nitrogen, Phosphorus, and Potassium levels.`;

  return (
    <div className="card border-success shadow-lg mt-4 overflow-hidden">
      {/* Header with Icon and Voice Trigger */}
      <div className="card-header bg-success text-white d-flex justify-content-between align-items-center py-3">
        <h5 className="mb-0 fw-bold d-flex align-items-center">
          <Sprout className="me-2" size={24} />
          Recommended Crop / Peekacha Salla 🌾
        </h5>
        
        {/* This triggers the gTTS audio from the backend */}
        <VoiceButton 
          mode="output" 
          textToSpeak={voiceScript} 
        />
      </div>
      
      <div className="card-body bg-light text-center py-5">
        <div className="mb-3">
          <CheckCircle className="text-success" size={48} />
        </div>
        <h3 className="display-5 fw-bold text-success text-capitalize mb-2">
          {crop}
        </h3>
        <p className="lead text-muted px-3">
          Our Random Forest ML Model suggests this is the optimal choice for your field.
        </p>
      </div>

      <div className="card-footer bg-white border-top-0 text-center pb-3">
        <span className="badge bg-success-subtle text-success border border-success px-3 py-2">
          Yield Potential: High
        </span>
        <div className="mt-3">
          <small className="text-muted">
            Click <strong>"Salla aika"</strong> above to listen to this recommendation.
          </small>
        </div>
      </div>
    </div>
  );
};

export default CropResult;