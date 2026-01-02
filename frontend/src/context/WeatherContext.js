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
  const [loading, setLoading] = useState(false); // Added loading state for better UX
  const isAuthenticated = isUserLoggedIn();

  const fetchWeather = useCallback(async () => {
    if (!isAuthenticated) return;
    
    setLoading(true);
    try {
      const token = getToken();
      // Ensure this matches your Flask backend port (default 5000)
      const response = await axios.get('http://127.0.0.1:5000/weather/alert', {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      // The backend now sends city, temp, description, humidity, wind, alert, AND rainfall
      setWeatherData(response.data);

      // Alert Logic
      const alertText = response.data.alert?.toLowerCase() || "";
      if (alertText.includes('alert') || alertText.includes('warning')) {
        toast.warn(response.data.alert);
      }
    } catch (err) {
      console.error("Failed to fetch global weather data:", err);
      // Optional: set basic defaults if API fails entirely
    } finally {
      setLoading(false);
    }
  }, [isAuthenticated]);

  useEffect(() => {
    let intervalId = null;
    if (isAuthenticated) {
      fetchWeather();
      // Refresh every 15 minutes (900000ms)
      intervalId = setInterval(fetchWeather, 900000);
    } else {
      setWeatherData(null);
    }
    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isAuthenticated, fetchWeather]);

  // Provide data, loading state, and the refetch function to the whole app
  const value = { 
    weatherData, 
    loading, 
    refetchWeather: fetchWeather 
  };

  return (
    <WeatherContext.Provider value={value}>
      {children}
    </WeatherContext.Provider>
  );
};