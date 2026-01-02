"""
Application configuration using Pydantic Settings.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # PostgreSQL connection
    postgres_host: str = "ktxn258.duckdns.org"
    postgres_port: int = 6543
    postgres_user: str = "casaos"
    postgres_password: str = "casaos"
    postgres_database: str = "postgres"

    # Connection settings
    connection_timeout: int = 5
    statement_timeout: int = 5000  # milliseconds

    # Metrics configuration
    metrics_retention_days: int = 90
    metrics_collection_interval_minutes: int = 5

    # API settings
    api_title: str = "PostgreSQL Monitoring API"
    api_version: str = "1.0.0"
    api_rate_limit: str = "100/minute"

    # Security
    allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
