// src/components/FertilizerResult.js
import React from 'react';
const FertilizerResult = ({ fertilizer }) => {
  if (!fertilizer) return null;
  return (
    <div className="alert alert-info border-info mt-4">
      <h2 className="alert-heading h4 fw-bold">Fertilizer Plan: 🌱</h2>
      <p className="mb-0 fs-5 text-capitalize">{fertilizer}</p>
    </div>
  );
};
export default FertilizerResult;