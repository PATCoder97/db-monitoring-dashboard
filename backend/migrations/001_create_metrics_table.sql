-- Migration: Create metrics_history table for storing historical database metrics
-- Created: 2026-01-02
-- Issue: #4 - Metrics Storage & Scheduler

CREATE TABLE IF NOT EXISTS metrics_history (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    db_name VARCHAR(255) NOT NULL,
    metric_type VARCHAR(50) NOT NULL,  -- 'size', 'table_count', 'connections'
    value NUMERIC NOT NULL,
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Create indexes for efficient querying
CREATE INDEX IF NOT EXISTS idx_metrics_timestamp ON metrics_history(timestamp);
CREATE INDEX IF NOT EXISTS idx_metrics_db_name ON metrics_history(db_name);
CREATE INDEX IF NOT EXISTS idx_metrics_db_type ON metrics_history(db_name, metric_type);

-- Add comment
COMMENT ON TABLE metrics_history IS 'Stores historical metrics for database monitoring and trend analysis';
COMMENT ON COLUMN metrics_history.metric_type IS 'Type of metric: size, table_count, connections, etc.';
COMMENT ON COLUMN metrics_history.metadata IS 'Additional metadata in JSON format';
