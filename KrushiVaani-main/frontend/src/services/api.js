import apiClient from './apiClient'; // CORRECTED: Import from the new client file

const WEATHER_API_KEY = process.env.REACT_APP_WEATHER_API_KEY;

/**
 * Fetches live weather data for a given location.
 * @param {string} location - The city or village name.
 * @returns {Promise<object>} An object with temperature, humidity, and rainfall.
 */
export const getWeatherData = async (location) => {
  const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=${WEATHER_API_KEY}&units=metric`);
  if (!response.ok) {
    throw new Error('Could not fetch weather data. Please check the location.');
  }
  const data = await response.json();
  return {
    temperature: data.main.temp,
    humidity: data.main.humidity,
    rainfall: data.rain?.['1h'] || 70, // Using a fallback if no direct rain data
  };
};

/**
 * Gets both crop and fertilizer recommendations from the backend.
 * @param {object} data - Combined soil and weather data.
 * @returns {Promise<object>} The server response with crop and fertilizer predictions.
 */
export const getBothRecommendations = async (data) => {
  try {
    const response = await apiClient.post('/recommend_all', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to get recommendations.');
  }
};

/**
 * Gets only a fertilizer recommendation for a user-specified crop.
 * @param {object} data - Combined soil, weather, and crop data.
 * @returns {Promise<object>} The server response with fertilizer prediction.
 */
export const getFertilizerOnly = async (data) => {
  try {
    const response = await apiClient.post('/fertilizer/recommend', data);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'Failed to get fertilizer plan.');
  }
};