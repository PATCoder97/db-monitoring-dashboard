"""
Metrics API router for historical metrics queries.
"""
from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional
import logging
import re

from ..services.metrics_collector import get_metrics_history, collect_metrics
from pydantic import BaseModel

router = APIRouter(prefix="/api/metrics", tags=["metrics"])
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
    if len(name) > 63:
        raise HTTPException(
            status_code=400,
            detail=f"Database name too long: '{name}'. Maximum 63 characters allowed."
        )
    return name


class MetricRecord(BaseModel):
    """Single metric record."""
    timestamp: str
    db_name: str
    metric_type: str
    value: float
    metadata: Optional[dict] = None


@router.post("/collect")
async def trigger_metrics_collection():
    """
    Manually trigger metrics collection for all databases.

    Returns:
        Status message
    """
    try:
        collect_metrics()
        return {"status": "success", "message": "Metrics collection completed"}
    except Exception as e:
        logger.error(f"Failed to collect metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to collect metrics: {str(e)}")


@router.get("/history/{db_name}", response_model=List[MetricRecord])
async def get_database_metrics_history(
    db_name: str = Path(..., description="Database name", min_length=1, max_length=63),
    metric_type: Optional[str] = Query(None, description="Filter by metric type (size, table_count, etc.)"),
    days: int = Query(7, ge=1, le=365, description="Number of days of history")
):
    """
    Get historical metrics for a specific database.

    Args:
        db_name: Database name (alphanumeric, underscore, hyphen only)
        metric_type: Optional filter by metric type
        days: Number of days of history (1-365)

    Returns:
        List of historical metric records
    """
    db_name = validate_database_name(db_name)
    try:
        metrics = get_metrics_history(db_name, metric_type, days)
        return metrics
    except Exception as e:
        logger.error(f"Failed to get metrics history for '{db_name}': {e}")
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {str(e)}")
