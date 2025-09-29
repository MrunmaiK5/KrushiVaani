import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-dark text-white text-center py-3 mt-auto">
      <div className="container">
        <p className="mb-0">
          &copy; {currentYear} KrushiVaani. All Rights Reserved.
        </p>
        <p className="mb-0 small">
          Your AI Farming Assistant
        </p>
      </div>
    </footer>
  );
};

export default Footer;