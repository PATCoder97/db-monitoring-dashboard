/**
 * Custom React Query hooks for database data fetching
 */
import { useQuery, UseQueryResult } from '@tanstack/react-query';
import { fetchDatabases, fetchDatabaseDetail, fetchMetricsHistory } from '../api/client';
import type { DatabaseSummary, DatabaseDetail, MetricRecord } from '../api/types';

/**
 * Hook to fetch all databases with auto-refresh support
 */
export const useDatabases = (autoRefresh: boolean = true) => {
  return useQuery<DatabaseSummary[], Error>({
    queryKey: ['databases'],
    queryFn: fetchDatabases,
    refetchInterval: autoRefresh ? 30000 : false, // 30 seconds
    staleTime: 10000, // Consider data stale after 10 seconds
  });
};

/**
 * Hook to fetch database details
 */
export const useDatabaseDetail = (name: string): UseQueryResult<DatabaseDetail, Error> => {
  return useQuery<DatabaseDetail, Error>({
    queryKey: ['database', name],
    queryFn: () => fetchDatabaseDetail(name),
    enabled: Boolean(name), // Only fetch if name is provided
  });
};

/**
 * Hook to fetch metrics history
 */
export const useMetricsHistory = (
  dbName: string,
  metricType?: string,
  days: number = 7
): UseQueryResult<MetricRecord[], Error> => {
  return useQuery<MetricRecord[], Error>({
    queryKey: ['metrics', dbName, metricType, days],
    queryFn: () => fetchMetricsHistory(dbName, metricType, days),
    enabled: Boolean(dbName),
  });
};
