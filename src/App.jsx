import React, { useState, useEffect } from 'react';
import TrendDashboard from './components/TrendDashboard';
import './App.css';

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setTimeout(() => setLoading(false), 1000);
  }, []);

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <header className="bg-gray-800 p-4 shadow-lg">
        <h1 className="text-3xl font-bold text-center text-teal-400">TrendPulse</h1>
        <p className="text-center text-gray-400">Real-Time Trend Prediction from Reddit & YouTube</p>
      </header>
      {loading ? (
        <div className="flex justify-center items-center h-screen">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-teal-400"></div>
        </div>
      ) : (
        <TrendDashboard />
      )}
    </div>
  );
}

export default App;