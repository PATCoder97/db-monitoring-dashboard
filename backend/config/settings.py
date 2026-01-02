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

    # API settings
    api_title: str = "PostgreSQL Monitoring API"
    api_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
