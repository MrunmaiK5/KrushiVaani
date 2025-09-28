import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Import Layout Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Import Page Components
import HomePage from './pages/Home';
import RecommendationPage from './pages/RecommendationPage'; // IMPORT NEW PAGE
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
            <Route path="/" element={<HomePage />} />
            {/* UPDATED ROUTE */}
            <Route path="/recommendation" element={<RecommendationPage />} />
            <Route path="/disease-detection" element={<DiseaseDetection />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/signup" element={<SignupPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;