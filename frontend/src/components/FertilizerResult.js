// // src/components/FertilizerResult.js
// import React from 'react';
// const FertilizerResult = ({ fertilizer }) => {
//   if (!fertilizer) return null;
//   return (
//     <div className="alert alert-info border-info mt-4">
//       <h2 className="alert-heading h4 fw-bold">Fertilizer Plan: 🌱</h2>
//       <p className="mb-0 fs-5 text-capitalize">{fertilizer}</p>
//     </div>
//   );
// };
// export default FertilizerResult;


import React from 'react';
import VoiceButton from './VoiceButton'; // Import our dual-mode voice button
import { Droplet, Info } from 'lucide-react'; // Professional farming icons

const FertilizerResult = ({ fertilizer }) => {
  if (!fertilizer) return null;

  // The natural language script for the AI to speak
  const voiceScript = `Based on your soil's nutrient requirements, the recommended fertilizer plan is: ${fertilizer}. Please ensure even application for the best results.`;

  return (
    <div className="card border-info shadow-lg mt-4 overflow-hidden">
      {/* Header with High Contrast and Voice Playback */}
      <div className="card-header bg-info text-white d-flex justify-content-between align-items-center py-3">
        <h5 className="mb-0 fw-bold d-flex align-items-center">
          <Droplet className="me-2" size={24} />
          Fertilizer Plan / Khatacha Salla 🌱
        </h5>
        
        {/* Sends the script to the backend gTTS service */}
        <VoiceButton 
          mode="output" 
          textToSpeak={voiceScript} 
        />
      </div>
      
      <div className="card-body bg-light">
        <div className="d-flex align-items-start gap-3 p-3 bg-white rounded border border-info-subtle">
          <div className="bg-info-subtle p-2 rounded">
            <Info className="text-info" size={32} />
          </div>
          <div>
            <p className="mb-0 fs-4 fw-bold text-dark text-capitalize">
              {fertilizer}
            </p>
            <p className="text-muted small mt-1">
              Recommended dosage based on your N-P-K values.
            </p>
          </div>
        </div>
      </div>

      <div className="card-footer bg-white border-top-0 py-3">
        <div className="d-flex justify-content-center">
          <small className="text-muted">
            Click <strong>"Salla aika"</strong> to hear the application instructions.
          </small>
        </div>
      </div>
    </div>
  );
};

export default FertilizerResult;