"""
Metrics collection service for periodic database monitoring.
Collects and stores metrics to metrics_history table.
"""
import psycopg2
from psycopg2 import Error
from psycopg2.extras import Json
from datetime import datetime, timedelta
import logging
from typing import Dict, List

from ..db_client import list_all_databases, get_connection_params

logger = logging.getLogger(__name__)


def store_metric(db_name: str, metric_type: str, value: float, metadata: Dict = None):
    """
    Store a single metric to the metrics_history table.

    Args:
        db_name: Name of the database
        metric_type: Type of metric (size, table_count, etc.)
        value: Numeric value of the metric
        metadata: Optional additional metadata
    """
    connection_params = get_connection_params('casaos')  # Use casaos DB for metrics storage

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Insert metric (use Json adapter for JSONB column)
        cursor.execute("""
            INSERT INTO metrics_history (db_name, metric_type, value, metadata)
            VALUES (%s, %s, %s, %s)
        """, (db_name, metric_type, value, Json(metadata) if metadata else None))

        connection.commit()
        cursor.close()
        connection.close()

        logger.debug(f"Stored metric: {db_name}.{metric_type} = {value}")

    except Error as e:
        logger.error(f"Failed to store metric: {e}")
        raise


def parse_size_to_bytes(size_str: str) -> int:
    """
    Convert PostgreSQL size string (e.g., '7475 kB') to bytes.

    Args:
        size_str: Size string from pg_size_pretty

    Returns:
        Size in bytes
    """
    size_str = size_str.strip()
    parts = size_str.split()

    if len(parts) != 2:
        return 0

    try:
        value = float(parts[0])
        unit = parts[1].upper()

        multipliers = {
            'BYTES': 1,
            'KB': 1024,
            'MB': 1024 ** 2,
            'GB': 1024 ** 3,
            'TB': 1024 ** 4
        }

        return int(value * multipliers.get(unit, 1))
    except (ValueError, KeyError):
        return 0


def collect_metrics():
    """
    Collect current metrics from all databases and store them.
    This function is called periodically by the scheduler.
    """
    logger.info("Starting metrics collection...")

    try:
        # Get all databases
        databases = list_all_databases()

        metrics_collected = 0
        for db in databases:
            db_name = db['name']

            # Store database size metric
            if 'size_bytes' in db:
                store_metric(
                    db_name=db_name,
                    metric_type='size',
                    value=db['size_bytes'],
                    metadata={'size_pretty': db['size']}
                )
                metrics_collected += 1

            # Store table count metric (if available)
            if 'table_count' in db and db['table_count'] is not None:
                store_metric(
                    db_name=db_name,
                    metric_type='table_count',
                    value=db['table_count']
                )
                metrics_collected += 1

            # Store connection limit metric
            if 'connection_limit' in db:
                store_metric(
                    db_name=db_name,
                    metric_type='connection_limit',
                    value=db['connection_limit']
                )
                metrics_collected += 1

        logger.info(f"Metrics collection complete: {metrics_collected} metrics stored from {len(databases)} databases")

    except Exception as e:
        logger.error(f"Metrics collection failed: {e}")


def cleanup_old_metrics(retention_days: int = 90):
    """
    Delete metrics older than the retention period.

    Args:
        retention_days: Number of days to retain metrics
    """
    connection_params = get_connection_params('casaos')

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Delete old metrics
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        cursor.execute("""
            DELETE FROM metrics_history
            WHERE timestamp < %s
        """, (cutoff_date,))

        deleted_count = cursor.rowcount
        connection.commit()
        cursor.close()
        connection.close()

        logger.info(f"Cleaned up {deleted_count} old metrics (retention: {retention_days} days)")

    except Error as e:
        logger.error(f"Failed to cleanup old metrics: {e}")


def get_metrics_history(db_name: str, metric_type: str = None, days: int = 7) -> List[Dict]:
    """
    Retrieve historical metrics for a database.

    Args:
        db_name: Database name
        metric_type: Optional filter by metric type
        days: Number of days of history to retrieve

    Returns:
        List of metric records
    """
    connection_params = get_connection_params('casaos')

    try:
        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Build query
        if metric_type:
            query = """
                SELECT timestamp, db_name, metric_type, value, metadata
                FROM metrics_history
                WHERE db_name = %s AND metric_type = %s
                  AND timestamp > NOW() - INTERVAL '%s days'
                ORDER BY timestamp ASC
            """
            cursor.execute(query, (db_name, metric_type, days))
        else:
            query = """
                SELECT timestamp, db_name, metric_type, value, metadata
                FROM metrics_history
                WHERE db_name = %s
                  AND timestamp > NOW() - INTERVAL '%s days'
                ORDER BY timestamp ASC
            """
            cursor.execute(query, (db_name, days))

        results = []
        for row in cursor.fetchall():
            results.append({
                'timestamp': row[0].isoformat(),
                'db_name': row[1],
                'metric_type': row[2],
                'value': float(row[3]),
                'metadata': row[4]
            })

        cursor.close()
        connection.close()

        logger.info(f"Retrieved {len(results)} metrics for {db_name}")
        return results

    except Error as e:
        logger.error(f"Failed to get metrics history: {e}")
        return []
