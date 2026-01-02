"""
Database API router with endpoints for listing and querying databases.
"""
from fastapi import APIRouter, HTTPException
from typing import List
import logging

from ..models import DatabaseSummary, DatabaseDetail, TableInfo
from ..db_client import list_all_databases, check_database_details, get_database_tables

router = APIRouter(prefix="/api", tags=["databases"])
logger = logging.getLogger(__name__)


@router.get("/databases", response_model=List[DatabaseSummary])
async def get_databases():
    """
    List all databases on the PostgreSQL server.

    Returns:
        List of database summaries with name, size, and status
    """
    try:
        databases = list_all_databases()
        return databases
    except Exception as e:
        logger.error(f"Failed to list databases: {e}")
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


@router.get("/databases/{name}", response_model=DatabaseDetail)
async def get_database(name: str):
    """
    Get detailed information about a specific database.

    Args:
        name: Database name

    Returns:
        Database details including version, encoding, and table list
    """
    try:
        details = check_database_details(name)
        return details
    except Exception as e:
        logger.error(f"Failed to get database details for '{name}': {e}")
        raise HTTPException(
            status_code=404 if "does not exist" in str(e) else 503,
            detail=f"Failed to retrieve database '{name}': {str(e)}"
        )


@router.get("/databases/{name}/tables", response_model=List[TableInfo])
async def get_tables(name: str):
    """
    Get table listing for a specific database.

    Args:
        name: Database name

    Returns:
        List of tables with row counts
    """
    try:
        tables = get_database_tables(name)
        return tables
    except Exception as e:
        logger.error(f"Failed to get tables for '{name}': {e}")
        raise HTTPException(
            status_code=404 if "does not exist" in str(e) else 503,
            detail=f"Failed to retrieve tables for '{name}': {str(e)}"
        )
