"""
Database connection and session management module.

This module sets up the SQLAlchemy database connection, session factory,
and provides a dependency function for FastAPI to manage database sessions.
"""

from typing import Generator  # For type hinting the generator function

# SQLAlchemy imports
from sqlalchemy import create_engine, Engine  # Core SQLAlchemy functionality
from sqlalchemy.ext.declarative import declarative_base  # For creating declarative models
from sqlalchemy.orm import sessionmaker, Session  # For creating and typing sessions

# Application settings
from app.core.config import settings

# Create a SQLAlchemy engine instance
# The engine is the starting point for any SQLAlchemy application
# It maintains a pool of connections to the database
engine: Engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,  # Database connection string from settings
    # Enables connection pool "pre-ping" feature that tests connections for liveness
    pool_pre_ping=True
)

# Create a sessionmaker factory
# This factory creates new Session objects when called
SessionLocal = sessionmaker(
    autocommit=False,  # Transactions are not auto-committed
    autoflush=False,   # Changes are not automatically flushed
    bind=engine        # Bind the session to our engine
)

# Create a base class for declarative models
# All database models will inherit from this base class
Base = declarative_base()

# FastAPI dependency for database sessions
def get_db() -> Generator[Session, None, None]:
    """
    Provide a SQLAlchemy session as a FastAPI dependency.

    Creates a new SQLAlchemy Session that is used for a single request,
    and then closed once the request is finished.

    Yields:
        Session: A SQLAlchemy Session instance

    Example:
        ```python
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
        ```
    """
    db: Session = SessionLocal()  # Create a new session
    try:
        yield db  # Use the session in the request
    finally:
        db.close()  # Ensure the session is closed after the request
