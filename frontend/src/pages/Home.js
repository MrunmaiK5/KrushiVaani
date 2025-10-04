import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';
import { isUserLoggedIn, getUser } from '../services/authorize';
import { useWeather } from '../context/WeatherContext';

function Home() {
  const isAuthenticated = isUserLoggedIn();
  const user = getUser();
  // Correctly destructure the weatherData from the context
  const { weatherData } = useWeather(); 

  const isCriticalAlert = (alertText) => {
    if (!alertText) return false;
    const criticalIcons = ['🔥', '🌧️', '💨', '❄️', '💧'];
    return criticalIcons.some(icon => alertText.includes(icon));
  };

  const hasCriticalAlert = weatherData && isCriticalAlert(weatherData.alert);
  
  const initialFeatures = [
    {
      title: 'Farm Analysis',
      description: 'Get a complete crop and fertilizer plan based on your soil data and local weather.',
      link: '/recommendation',
      icon: '📊',
    },
    {
      title: 'Disease Detection',
      description: 'Upload an image of a plant leaf to detect diseases early and get treatment advice.',
      link: '/disease-detection',
      icon: '🔍',
    },
    {
      title: 'Weather Alerts',
      description: 'Stay updated with real-time weather forecasts and alerts for your location.',
      link: '/weather-alert',
      icon: '🌦️',
    },
    {
      title: 'AI Chatbot',
      description: 'Have a question? Ask our AI-powered chatbot for instant agricultural advice.',
      link: '/chatbot',
      icon: '🤖',
    },
    {
      title: 'Login',
      description: 'Access your account or register to save your data and preferences.',
      link: '/login',
      icon: '👤',
    },
  ];

  const features = isAuthenticated 
    ? initialFeatures.filter(feature => feature.title !== 'Login') 
    : initialFeatures;

  return (
    <>
      {/* Hero Section */}
      <header className="hero-section text-white text-center d-flex flex-column justify-content-center align-items-center">
        <div className="container">
          {isAuthenticated && user ? (
            <>
              <h1 className="display-4 fw-bold">Welcome back, {user.username}!</h1>
              <p className="lead col-lg-8 mx-auto">
                Ready to get new insights for your farm?
              </p>
              <Link to="/recommendation" className="btn btn-success btn-lg mt-3">
                Go to Farm Analysis
              </Link>
            </>
          ) : (
            <>
              <h1 className="display-4 fw-bold">Welcome to KrushiVaani</h1>
              <p className="lead col-lg-8 mx-auto">
                Your personal AI-powered farming assistant. We provide data-driven insights to help you cultivate a better harvest.
              </p>
              <Link to="/login" className="btn btn-success btn-lg mt-3">
                Get Started
              </Link>
            </>
          )}
        </div>
      </header>

      {/* Main Content Container */}
      <div className="container my-5">
        
        {/* Dynamic Alert Banner */}
        {isAuthenticated && hasCriticalAlert && (
          <div className="alert alert-danger text-center shadow-sm" role="alert">
            <strong>Weather Alert:</strong> {weatherData.alert} <Link to="/weather-alert" className="alert-link">More Info</Link>
          </div>
        )}
        
        <div className="alert alert-warning text-center shadow-sm mt-4" role="alert">
          <strong>Please note:</strong> To use this website, you'll need a verified soil report from a trusted organization.
        </div>

        <h2 className="text-center fw-bold mb-5 mt-5">Our Features</h2>
        <div className="row g-4">
          {features.map((feature, index) => (
            <div key={index} className="col-lg-4 col-md-6 d-flex">
              <div className="card h-100 text-center shadow-sm border-0 feature-card w-100">
                <div className="card-body p-4 d-flex flex-column">
                  <div className="feature-icon mb-3">{feature.icon}</div>
                  <h5 className="card-title fw-bold">{feature.title}</h5>
                  <p className="card-text text-muted">{feature.description}</p>
                  <Link to={feature.link} className="btn btn-outline-success mt-auto">
                    Explore
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </>
  );
};

export default Home;