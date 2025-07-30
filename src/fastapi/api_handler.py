# src/fastapi/api_handler.py
# =======================================================================
# 📝 FILE OVERVIEW
# =======================================================================
"""
This file serves as the main entry point for the FastAPI application.

It defines the FastAPI app factory, initializes the application instance,
configures middleware, and wires up all the API routers.
"""

# =======================================================================
# ⚙️ 1. IMPORTS & INITIALIZATION
# =======================================================================
import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.services.health.routers.health import router as health_router
from src.services.items.routers.items import router as items_router
from src.database.database import create_db_and_tables  # Import the new function
from src.utils.logging import configure_logging

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

# Comma-separated list from environment variable
ALLOWED_CORS_ORIGINS = os.getenv("ALLOWED_CORS_ORIGINS", "*").strip().split(",")


# =======================================================================
# 🏭 2. FASTAPI APP FACTORY
# =======================================================================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle startup and shutdown events.
    """
    logger.info("Creating database tables (if they don't exist)...")
    create_db_and_tables()
    logger.info("Database tables created.")
    yield
    logger.info("Application shutdown.")


def create_app(routers: list) -> FastAPI:
    """
    Creates and configures a new FastAPI application instance.

    Args:
        routers: A list of FastAPI APIRouter objects to be included.

    Returns:
        The configured FastAPI application instance.
    """
    tags_metadata = []

    app = FastAPI(
        openapi_version="3.0.3",
        openapi_tags=tags_metadata,
        lifespan=lifespan,
        logger=logger,
    )

    for router in routers:
        app.include_router(router)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app


# =======================================================================
#  🚀 3. FastAPI APPLICATION SETUP
# =======================================================================
# Create the main FastAPI application instance by aggregating all the
# service routers.
app = create_app(routers=[health_router, items_router])
