/**
 * Database card component with memoization
 */
import React from 'react';
import StatusBadge from './StatusBadge';
import type { DatabaseSummary } from '../api/types';

interface DatabaseCardProps extends DatabaseSummary {
  onClick?: () => void;
}

const DatabaseCard: React.FC<DatabaseCardProps> = React.memo(({ name, size, status, table_count, onClick }) => {
  return (
    <div
      className="p-6 border border-gray-200 rounded-lg shadow hover:shadow-lg transition-shadow cursor-pointer bg-white"
      onClick={onClick}
    >
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-xl font-bold text-gray-900">{name}</h3>
        <StatusBadge status={status} />
      </div>

      <div className="space-y-2 text-sm text-gray-600">
        <div className="flex justify-between">
          <span>Size:</span>
          <span className="font-medium text-gray-900">{size}</span>
        </div>
        <div className="flex justify-between">
          <span>Tables:</span>
          <span className="font-medium text-gray-900">{table_count}</span>
        </div>
      </div>
    </div>
  );
});

DatabaseCard.displayName = 'DatabaseCard';

export default DatabaseCard;
