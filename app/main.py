"""Main application module for the FastAPI microservice.

This module initializes the FastAPI application, sets up middleware,
configures logging, metrics, and registers API routes.
"""

from typing import Dict  # Standard library imports for type hints

# FastAPI framework imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # For handling Cross-Origin Resource Sharing

# Application-specific imports
from app.api.api_v1.api import api_router  # Router containing all API endpoints
from app.core.config import settings  # Application configuration settings
from app.core.logging import configure_logging, get_logger  # Logging utilities
from app.core.metrics import setup_metrics  # Prometheus metrics setup

# Configure application logging
configure_logging()  # Set up logging based on application settings
logger = get_logger(__name__)  # Get a logger instance for this module

# Initialize the FastAPI application with configuration settings
app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,  # Application name from settings
    openapi_url=f"{settings.API_V1_STR}/openapi.json",  # URL for OpenAPI documentation
    version="0.1.0"  # Should match the version in pyproject.toml
)

# Register startup event handler
# This function will be called when the application starts
@app.on_event("startup")
async def startup_event() -> None:
    """Startup event handler that runs when the application starts.

    Used for initialization tasks like connecting to databases.
    """
    logger.info(
        "Starting up application",
        environment=settings.ENVIRONMENT
    )

# Register shutdown event handler
# This function will be called when the application shuts down
@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Shutdown event handler that runs when the application stops.

    Used for cleanup tasks like closing database connections.
    """
    logger.info("Shutting down application")

# Set up Cross-Origin Resource Sharing (CORS) middleware
# This allows the API to be called from different origins (domains)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,  # List of allowed origins from settings
    allow_credentials=True,  # Allow cookies in CORS requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all HTTP headers
)

# Set up Prometheus metrics for monitoring application performance
setup_metrics(app, settings.PROJECT_NAME, app.version)

# Root endpoint - serves as a simple landing page for the API
@app.get("/")
def root() -> Dict[str, str]:
    """Root endpoint that returns a simple greeting message.

    This can be used to verify that the API is running.
    """
    return {"message": "Hello World"}

# Health check endpoints for monitoring and orchestration

@app.get("/health")
def health_check() -> Dict[str, str]:
    """Health check endpoint for monitoring.

    Returns a simple status to indicate the service is running.
    """
    return {"status": "ok"}

@app.get("/health/readiness")
def readiness_check() -> Dict[str, str]:
    """Readiness check endpoint for Kubernetes.

    Indicates whether the service is ready to accept requests.
    This can include checks for database connections, etc.
    """
    # Add any additional readiness checks here (e.g., database connection)
    return {"status": "ready"}

@app.get("/health/liveness")
def liveness_check() -> Dict[str, str]:
    """Liveness check endpoint for Kubernetes.

    Indicates whether the service is alive and functioning.
    Used by orchestration systems to determine if the service needs to be restarted.
    """
    return {"status": "alive"}

# Include API routers
# This registers all the API endpoints defined in the api_v1 module
app.include_router(
    api_router,  # Router containing all API endpoints
    prefix=settings.API_V1_STR  # Prefix all routes with the API version (e.g., /api/v1)
)

# Entry point for running the application directly (not through a WSGI server)
if __name__ == "__main__":
    import uvicorn  # ASGI server for running FastAPI applications
    # Run the application with uvicorn, enabling hot reloading for development
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
