/**
 * TypeScript interfaces for API responses
 */

export interface DatabaseSummary {
  name: string;
  size: string;
  status: 'ok' | 'warning' | 'error';
  table_count: number;
}

export interface TableInfo {
  name: string;
  row_count: number;
}

export interface DatabaseDetail {
  name: string;
  version: string;
  encoding: string;
  size: string;
  tables: TableInfo[];
  table_count: number;
}

export interface MetricRecord {
  timestamp: string;
  db_name: string;
  metric_type: string;
  value: number;
  metadata?: Record<string, any>;
}

export interface HealthResponse {
  status: string;
  database: string;
}
