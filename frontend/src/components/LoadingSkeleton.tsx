/**
 * Loading skeleton for database cards
 */
import React from 'react';

const LoadingSkeleton: React.FC = () => {
  return (
    <div className="p-6 border border-gray-200 rounded-lg shadow animate-pulse">
      <div className="h-4 bg-gray-200 rounded w-20 mb-4"></div>
      <div className="h-6 bg-gray-200 rounded w-32 mb-3"></div>
      <div className="h-4 bg-gray-200 rounded w-24 mb-2"></div>
      <div className="h-4 bg-gray-200 rounded w-28"></div>
    </div>
  );
};

export default LoadingSkeleton;
