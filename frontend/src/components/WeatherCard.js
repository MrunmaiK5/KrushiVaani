import React from 'react';
import { useWeather } from '../context/WeatherContext';
import './WeatherCard.css';

function WeatherCard() {
  const { weatherData } = useWeather(); // <-- DESTRUCTURE to get weatherData

  const getCardStyle = () => {
    if (!weatherData || !weatherData.alert) return 'card-info';
    const alertText = weatherData.alert.toLowerCase();
    if (alertText.includes('alert') || alertText.includes('warning')) {
      return 'card-danger';
    }
    return 'card-success';
  };

  if (!weatherData) {
    return <div>Loading weather data...</div>;
  }

  return (
    <div className={`weather-card ${getCardStyle()}`}>
      <h3>Weather in {weatherData.city}</h3>
      <p className="temperature">{weatherData.temperature}°C</p>
      <p className="description">{weatherData.description}</p>
      <hr />
      <p className="alert-message"><strong>Update:</strong> {weatherData.alert}</p>
    </div>
  );
}

export default WeatherCard;