"""
Database API router with endpoints for listing and querying databases.
"""
from fastapi import APIRouter, HTTPException, Path
from typing import List
import logging
import re

from ..models import DatabaseSummary, DatabaseDetail, TableInfo
from ..db_client import list_all_databases, check_database_details, get_database_tables

router = APIRouter(prefix="/api", tags=["databases"])
logger = logging.getLogger(__name__)


def validate_database_name(name: str) -> str:
    """
    Validate database name to prevent SQL injection.

    Args:
        name: Database name to validate

    Returns:
        Validated name

    Raises:
        HTTPException: If name is invalid
    """
    if not re.match(r'^[a-zA-Z0-9_-]+$', name):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid database name: '{name}'. Only alphanumeric characters, underscores, and hyphens are allowed."
        )
    if len(name) > 63:  # PostgreSQL identifier limit
        raise HTTPException(
            status_code=400,
            detail=f"Database name too long: '{name}'. Maximum 63 characters allowed."
        )
    return name


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
async def get_database(name: str = Path(..., description="Database name", min_length=1, max_length=63)):
    """
    Get detailed information about a specific database.

    Args:
        name: Database name (alphanumeric, underscore, hyphen only)

    Returns:
        Database details including version, encoding, and table list
    """
    name = validate_database_name(name)
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
async def get_tables(name: str = Path(..., description="Database name", min_length=1, max_length=63)):
    """
    Get table listing for a specific database.

    Args:
        name: Database name (alphanumeric, underscore, hyphen only)

    Returns:
        List of tables with row counts
    """
    name = validate_database_name(name)
    try:
        tables = get_database_tables(name)
        return tables
    except Exception as e:
        logger.error(f"Failed to get tables for '{name}': {e}")
        raise HTTPException(
            status_code=404 if "does not exist" in str(e) else 503,
            detail=f"Failed to retrieve tables for '{name}': {str(e)}"
        )
