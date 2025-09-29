import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Import Layout and Page Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';
import ProtectedRoute from './components/ProtectedRoute'; // <-- 1. IMPORT
import HomePage from './pages/Home';
import RecommendationPage from './pages/RecommendationPage';
import DiseaseDetection from './pages/DiseaseDetection';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';

function App() {
  return (
    <Router>
      <div className="d-flex flex-column min-vh-100">
        <Navbar />
        <main className="flex-grow-1">
          <Routes>
            {/* These routes are PUBLIC */}
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />

            {/* 2. WRAP YOUR PROTECTED ROUTES */}
            <Route 
              path="/recommendation" 
              element={
                <ProtectedRoute>
                  <RecommendationPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/disease-detection" 
              element={
                <ProtectedRoute>
                  <DiseaseDetection />
                </ProtectedRoute>
              } 
            />
            {/* You can also protect the Weather and Chatbot pages the same way */}

          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;