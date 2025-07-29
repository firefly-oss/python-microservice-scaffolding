"""
Database initialization module.

This module provides functionality to initialize the database schema
and populate it with initial data when the application starts.
"""

from sqlalchemy.orm import Session  # SQLAlchemy session for database operations

# Application imports
from app import repositories, schemas  # Repository operations and Pydantic schemas
from app.core.config import settings  # Application settings
from app.models import Base  # SQLAlchemy models base class
from app.db.database import engine  # Database engine


def init_db(db: Session) -> None:
    """
    Initialize the database with tables and seed data.

    This function performs two main tasks:
    1. Creates all database tables defined in the models if they don't exist
    2. Seeds the database with initial data if needed

    Args:
        db: SQLAlchemy database session

    Note:
        This function is typically called during application startup
        to ensure the database is properly set up before handling requests.
    """
    # Create all tables defined in the models
    # This is equivalent to running migrations to create the schema
    # If tables already exist, this operation will not affect them
    Base.metadata.create_all(bind=engine)

    # Create initial data if needed (seed data)
    # This is useful for populating lookup tables, default settings,
    # or creating test data in development environments

    # Example: Create a default test item if it doesn't exist
    item = repositories.item.get_by_name(db, name="Test Item")
    if not item:
        # Create a Pydantic schema with the item data
        item_in = schemas.ItemCreate(
            name="Test Item",
            description="This is a test item",
            is_active=True,
        )
        # Use the repository to create the item in the database
        repositories.item.create(db=db, obj_in=item_in)
