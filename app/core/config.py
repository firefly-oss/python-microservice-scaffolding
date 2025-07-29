"""Configuration module for the application.

This module defines application settings using Pydantic's BaseSettings,
which allows for environment variable overrides and validation.
"""

from typing import Any, Dict, List, Optional, Union  # Standard library imports for type hints
from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator  # Pydantic for settings management


class Settings(BaseSettings):
    """
    Application settings class that handles configuration from environment variables.

    This class defines all configurable parameters for the application, with defaults
    that can be overridden by environment variables or a .env file.
    """
    # API configuration
    API_V1_STR: str = "/api/v1"  # URL prefix for API version 1
    PROJECT_NAME: str = "Microservice Scaffolding"  # Name of the project
    ENVIRONMENT: str = "development"  # Current environment (development, staging, production)

    # CORS Configuration - Cross-Origin Resource Sharing
    # List of origins that are allowed to make requests to this API
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Convert string input to a list for CORS origins.

        Args:
            v: The value to validate, either a comma-separated string or a list

        Returns:
            A list of CORS origins

        Raises:
            ValueError: If the input is not a valid string or list
        """
        if isinstance(v, str) and not v.startswith("["):
            # Convert comma-separated string to list
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            # Return as is if already a list or a string representation of a list
            return v
        raise ValueError(v)

    # Database Configuration
    POSTGRES_SERVER: str = "localhost"  # PostgreSQL server hostname
    POSTGRES_USER: str = "postgres"  # PostgreSQL username
    POSTGRES_PASSWORD: str = "postgres"  # PostgreSQL password
    POSTGRES_DB: str = "app"  # PostgreSQL database name
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None  # Full database connection URI

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """
        Build a PostgreSQL connection URI from individual components.

        Args:
            v: The existing URI value, if any
            values: Dictionary of settings values

        Returns:
            A complete PostgreSQL connection URI
        """
        if isinstance(v, str):
            # Return as is if already a complete URI string
            return v
        # Build URI from individual components
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        """
        Pydantic configuration for the Settings class.
        """
        case_sensitive = True  # Environment variable names are case-sensitive
        env_file = ".env"  # Load settings from .env file if present


# Create a global settings instance
settings: Settings = Settings()  # Initialize settings with defaults and environment overrides
