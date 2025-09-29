// src/components/CropResult.js
import React from 'react';
const CropResult = ({ crop }) => {
  if (!crop) return null;
  return (
    <div className="alert alert-success border-success mt-4">
      <h2 className="alert-heading h4 fw-bold">Recommended Crop: 🌾</h2>
      <p className="mb-0 fs-5 text-capitalize">{crop}</p>
    </div>
  );
};
export default CropResult;