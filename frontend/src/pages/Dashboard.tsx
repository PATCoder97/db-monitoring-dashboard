/**
 * Main dashboard page
 */
import React, { useState, useCallback } from 'react';
import { useDatabases } from '../hooks/useDatabases';
import DatabaseCard from '../components/DatabaseCard';
import SearchBar from '../components/SearchBar';
import LoadingSkeleton from '../components/LoadingSkeleton';
import ErrorDisplay from '../components/ErrorDisplay';

const Dashboard: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [autoRefresh, setAutoRefresh] = useState(true);

  const { data: databases, isLoading, error, refetch } = useDatabases(autoRefresh);

  // Filter databases based on search query
  const filteredDatabases = databases?.filter((db) =>
    db.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleSearch = useCallback((query: string) => {
    setSearchQuery(query);
  }, []);

  const handleDatabaseClick = (name: string) => {
    console.log('Database clicked:', name);
    // TODO: Navigate to database detail page
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Database Monitoring</h1>
              <p className="mt-1 text-sm text-gray-600">Monitor your PostgreSQL databases in real-time</p>
            </div>

            <div className="flex items-center gap-4">
              {/* Auto-refresh toggle */}
              <button
                onClick={() => setAutoRefresh(!autoRefresh)}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  autoRefresh
                    ? 'bg-blue-600 text-white hover:bg-blue-700'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {autoRefresh ? 'Auto-Refresh: ON' : 'Auto-Refresh: OFF'}
              </button>

              {/* Manual refresh */}
              <button
                onClick={() => refetch()}
                className="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
                title="Manual refresh"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                  />
                </svg>
              </button>
            </div>
          </div>

          {/* Search bar */}
          <div className="mt-6">
            <SearchBar onSearch={handleSearch} />
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Error state */}
        {error && (
          <ErrorDisplay
            message={error.message || 'Failed to load databases. Please check if the backend API is running.'}
            onRetry={() => refetch()}
          />
        )}

        {/* Loading state */}
        {isLoading && !databases && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <LoadingSkeleton key={i} />
            ))}
          </div>
        )}

        {/* Databases grid */}
        {!error && !isLoading && databases && (
          <>
            {filteredDatabases && filteredDatabases.length > 0 ? (
              <>
                <div className="mb-4 text-sm text-gray-600">
                  Showing {filteredDatabases.length} of {databases.length} database{databases.length !== 1 ? 's' : ''}
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {filteredDatabases.map((db) => (
                    <DatabaseCard
                      key={db.name}
                      {...db}
                      onClick={() => handleDatabaseClick(db.name)}
                    />
                  ))}
                </div>
              </>
            ) : (
              <div className="text-center py-12">
                <p className="text-gray-500">
                  {searchQuery ? `No databases found matching "${searchQuery}"` : 'No databases found'}
                </p>
              </div>
            )}
          </>
        )}

        {/* Auto-refresh indicator */}
        {autoRefresh && !error && (
          <div className="fixed bottom-4 right-4 bg-white border border-gray-200 rounded-lg shadow-lg px-4 py-2 text-sm text-gray-600">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              Auto-refreshing every 30s
            </div>
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
