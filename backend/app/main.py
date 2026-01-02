"""
FastAPI application for PostgreSQL Database Monitoring Dashboard.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .routers import databases
from .models import HealthResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="PostgreSQL Monitoring API",
    description="REST API for monitoring PostgreSQL databases",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(databases.router)


@app.get("/api/health", response_model=HealthResponse, tags=["health"])
async def health_check():
    """
    Health check endpoint.

    Returns:
        Health status of the API
    """
    return HealthResponse(status="healthy", message="PostgreSQL Monitoring API is running")


@app.get("/", tags=["root"])
async def root():
    """
    Root endpoint with API information.
    """
    return {
        "name": "PostgreSQL Monitoring API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }
