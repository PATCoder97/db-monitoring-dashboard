/**
 * API client for database monitoring backend
 */
import axios from 'axios';
import type { DatabaseSummary, DatabaseDetail, TableInfo, MetricRecord, HealthResponse } from './types';

// Create axios instance with base configuration
export const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetch all databases
 */
export const fetchDatabases = async (): Promise<DatabaseSummary[]> => {
  const { data } = await api.get<DatabaseSummary[]>('/databases');
  return data;
};

/**
 * Fetch details for a specific database
 */
export const fetchDatabaseDetail = async (name: string): Promise<DatabaseDetail> => {
  const { data } = await api.get<DatabaseDetail>(`/databases/${name}`);
  return data;
};

/**
 * Fetch tables for a specific database
 */
export const fetchDatabaseTables = async (name: string): Promise<TableInfo[]> => {
  const { data } = await api.get<TableInfo[]>(`/databases/${name}/tables`);
  return data;
};

/**
 * Fetch metrics history for a database
 */
export const fetchMetricsHistory = async (
  dbName: string,
  metricType?: string,
  days: number = 7
): Promise<MetricRecord[]> => {
  const params: Record<string, any> = { days };
  if (metricType) {
    params.metric_type = metricType;
  }

  const { data } = await api.get<MetricRecord[]>(`/metrics/history/${dbName}`, { params });
  return data;
};

/**
 * Trigger manual metrics collection
 */
export const triggerMetricsCollection = async (): Promise<{ status: string; message: string }> => {
  const { data } = await api.post('/metrics/collect');
  return data;
};

/**
 * Health check
 */
export const fetchHealth = async (): Promise<HealthResponse> => {
  const { data } = await api.get<HealthResponse>('/health');
  return data;
};
