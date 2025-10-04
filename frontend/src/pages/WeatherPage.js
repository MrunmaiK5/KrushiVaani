// frontend/src/pages/WeatherPage.js

import React from 'react';
import WeatherCard from '../components/WeatherCard'; // The component that fetches and displays weather

function WeatherPage() {
  return (
    <div className="container my-5">
      <div className="text-center">
        <h1 className="display-5 fw-bold">Live Weather Alerts</h1>
        <p className="lead text-muted mb-4">
          Stay updated with real-time weather conditions and alerts for your location.
        </p>
      </div>
      <div className="d-flex justify-content-center">
        <div style={{ width: '100%', maxWidth: '600px' }}>
          {/* This is the component that does all the work */}
          <WeatherCard />
        </div>
      </div>
    </div>
  );
}

export default WeatherPage;