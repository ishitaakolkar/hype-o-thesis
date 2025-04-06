import React, { useState, useEffect } from 'react';
import TrendCard from './TrendCard';

function TrendDashboard() {
  const [trends, setTrends] = useState([]);
  const [risingTrends, setRisingTrends] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch weekly trends from backend API
    fetch('/api/trends/week')
      .then((res) => res.json())
      .then((data) => {
        setTrends(data);
        // Filter rising trends (e.g., posts with increasing engagement)
        const rising = data.filter(trend => trend.engagementGrowth > 0.1); // 10% growth threshold
        setRisingTrends(rising);
        setLoading(false);
      })
      .catch((err) => console.error('Error fetching trends:', err));
  }, []);

  const predictTop3 = (trend) => {
    // Simple prediction logic based on engagement and growth
    const score = trend.engagement * (1 + trend.engagementGrowth) * (trend.sentimentScore || 0.5);
    return score > 0.8 ? 75 : Math.min(50 + score * 50, 75); // 75% max chance
  };

  if (loading) return <p className="text-center mt-10">Loading trends...</p>;

  return (
    <div className="container mx-auto p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-teal-300 mb-4">Weekly Top Trends</h2>
        <div className="flex space-x-4">
          <button className="bg-teal-600 hover:bg-teal-700 text-white py-2 px-4 rounded-lg transition duration-300">
            Filter: Week
          </button>
          <button className="bg-gray-700 hover:bg-gray-600 py-2 px-4 rounded-lg transition duration-300">
            Rising Trends
          </button>
        </div>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {risingTrends.map((trend) => (
          <TrendCard
            key={trend.id}
            title={trend.title}
            platform={trend.platform}
            engagement={trend.engagement}
            growth={trend.engagementGrowth}
            prediction={predictTop3(trend)}
          />
        ))}
      </div>
    </div>
  );
}

export default TrendDashboard;