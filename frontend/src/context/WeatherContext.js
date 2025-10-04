import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { isUserLoggedIn, getToken } from '../services/authorize';

const WeatherContext = createContext();

export const useWeather = () => {
  return useContext(WeatherContext);
};

export const WeatherProvider = ({ children }) => {
  const [weatherData, setWeatherData] = useState(null);
  const isAuthenticated = isUserLoggedIn();

  // We use useCallback to prevent this function from being recreated on every render
  const fetchWeather = useCallback(async () => {
    if (!isAuthenticated) return;
    try {
      const token = getToken();
      const response = await axios.get('http://127.0.0.1:5000/weather/alert', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      setWeatherData(response.data);

      const alertText = response.data.alert.toLowerCase();
      if (alertText.includes('alert') || alertText.includes('warning')) {
        toast.warn(response.data.alert);
      }
    } catch (err) {
      console.error("Failed to fetch global weather data:", err);
    }
  }, [isAuthenticated]); // This function depends on the login status

  useEffect(() => {
    let intervalId = null;
    if (isAuthenticated) {
      fetchWeather();
      intervalId = setInterval(fetchWeather, 900000);
    } else {
      setWeatherData(null);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isAuthenticated, fetchWeather]);

  // We now provide both the data AND the refetch function to the app
  const value = { weatherData, refetchWeather: fetchWeather };

  return (
    <WeatherContext.Provider value={value}>
      {children}
    </WeatherContext.Provider>
  );
};