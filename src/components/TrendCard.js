import React from 'react';

function TrendCard({ title, platform, engagement, growth, prediction }) {
  return (
    <div className="bg-gray-800 p-6 rounded-lg shadow-lg hover:shadow-xl transition-shadow duration-300">
      <h3 className="text-xl font-semibold text-teal-300 mb-2">{title}</h3>
      <p className="text-gray-400 mb-2">Platform: {platform}</p>
      <p className="text-gray-300 mb-2">Engagement: {engagement.toFixed(2)}k</p>
      <p className="text-gray-300 mb-2">Growth: {growth.toFixed(2)}%</p>
      <div className="mt-4">
        <p className="text-lg font-medium text-yellow-400">
          Prediction: {prediction}% chance to reach Top 3 this week!
        </p>
        <div className="w-full bg-gray-700 rounded-full h-2.5 mt-2">
          <div
            className="bg-teal-400 h-2.5 rounded-full transition-all duration-500"
            style={{ width: `${prediction}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
}

export default TrendCard;