"""
Database initialization module.

This module provides functions to initialize the database with initial data.
It can be run as a standalone script or imported and used by other modules.
"""

import logging

from app.db.database import SessionLocal
from app.db.init_db import init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    """
    Initialize the database with initial data.

    This function creates a database session, calls the init_db function
    to populate the database with initial data, and ensures the session
    is properly closed afterward.
    """
    db = SessionLocal()
    try:
        init_db(db)
        logger.info("Database initialized successfully")
    finally:
        db.close()


def main() -> None:
    """
    Main entry point for database initialization.

    This function logs the initialization process and calls the init function
    to perform the actual database initialization.
    """
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
