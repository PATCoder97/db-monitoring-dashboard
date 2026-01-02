"""
Pydantic models for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class TableInfo(BaseModel):
    """Information about a database table."""
    name: str
    type: str
    row_count: Optional[int] = None


class DatabaseSummary(BaseModel):
    """Summary information for a database (list view)."""
    name: str
    size: str  # Human-readable size (e.g., "10 MB")
    size_bytes: int  # Size in bytes for sorting/comparison
    collation: str
    connection_limit: int
    status: str = Field(default="ok", description="Health status: ok, warning, error")


class DatabaseDetail(BaseModel):
    """Detailed information for a single database."""
    name: str
    version: str
    encoding: str
    tables: List[TableInfo]
    table_count: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    message: str = "API is running"
