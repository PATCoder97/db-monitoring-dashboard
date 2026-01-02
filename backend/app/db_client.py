"""
Database client module for PostgreSQL monitoring.
Extracted from main.py and refactored for FastAPI usage.
"""
import os
import psycopg2
from psycopg2 import Error
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


def get_connection_params(database: str = 'postgres') -> dict:
    """Get database connection parameters from environment variables."""
    return {
        'host': os.getenv('POSTGRES_HOST', 'ktxn258.duckdns.org'),
        'port': int(os.getenv('POSTGRES_PORT', 6543)),
        'database': database,
        'user': os.getenv('POSTGRES_USER', 'casaos'),
        'password': os.getenv('POSTGRES_PASSWORD', 'casaos'),
        'connect_timeout': 5
    }


def list_all_databases() -> List[Dict[str, any]]:
    """
    List all databases in PostgreSQL server.

    Returns:
        List of dictionaries containing database information
    """
    connection_params = get_connection_params('postgres')

    try:
        logger.info(f"Connecting to {connection_params['host']}:{connection_params['port']}")

        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Get PostgreSQL version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        logger.info(f"Connected to PostgreSQL: {db_version[:80]}")

        # List all databases
        cursor.execute("""
            SELECT
                datname as database_name,
                pg_size_pretty(pg_database_size(datname)) as size,
                pg_database_size(datname) as size_bytes,
                datcollate as collation,
                datconnlimit as connection_limit
            FROM pg_database
            WHERE datistemplate = false
            ORDER BY datname;
        """)

        databases = []
        for row in cursor.fetchall():
            databases.append({
                'name': row[0],
                'size': row[1],
                'size_bytes': row[2],
                'collation': row[3],
                'connection_limit': row[4],
                'status': 'ok'  # Will be enhanced with health checks later
            })

        cursor.close()
        connection.close()

        logger.info(f"Successfully retrieved {len(databases)} databases")
        return databases

    except Error as e:
        logger.error(f"PostgreSQL error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


def check_database_details(db_name: str) -> Dict[str, any]:
    """
    Get detailed information about a specific database.

    Args:
        db_name: Name of the database to check

    Returns:
        Dictionary containing database details including tables
    """
    connection_params = get_connection_params(db_name)

    try:
        logger.info(f"Checking database: {db_name}")

        connection = psycopg2.connect(**connection_params)
        cursor = connection.cursor()

        # Get database version and settings
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]

        cursor.execute("SHOW server_encoding;")
        encoding = cursor.fetchone()[0]

        # Get list of tables
        cursor.execute("""
            SELECT
                table_name,
                table_type
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)

        tables = []
        for table_row in cursor.fetchall():
            table_name = table_row[0]
            table_type = table_row[1]

            # Get row count for each table
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
                row_count = cursor.fetchone()[0]
            except Exception as e:
                logger.warning(f"Could not count rows in {table_name}: {e}")
                row_count = None

            tables.append({
                'name': table_name,
                'type': table_type,
                'row_count': row_count
            })

        cursor.close()
        connection.close()

        result = {
            'name': db_name,
            'version': version,
            'encoding': encoding,
            'tables': tables,
            'table_count': len(tables)
        }

        logger.info(f"Retrieved details for {db_name}: {len(tables)} tables")
        return result

    except Error as e:
        logger.error(f"Cannot connect to database '{db_name}': {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


def get_database_tables(db_name: str) -> List[Dict[str, any]]:
    """
    Get just the table list for a database (lighter than full details).

    Args:
        db_name: Name of the database

    Returns:
        List of table information dictionaries
    """
    details = check_database_details(db_name)
    return details.get('tables', [])
