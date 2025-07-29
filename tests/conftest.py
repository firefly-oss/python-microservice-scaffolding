"""
Pytest configuration and fixtures for testing.

This module sets up the test environment, including:
1. An in-memory SQLite database for testing
2. Fixtures for database sessions and FastAPI test client
3. Dependency overrides to use the test database instead of the real one

These fixtures are automatically used by pytest when running tests.
"""

from typing import Generator  # Type hints

# Testing imports
import pytest  # Pytest framework
from fastapi.testclient import TestClient  # FastAPI test client

# SQLAlchemy imports
from sqlalchemy import create_engine, Engine  # Database engine
from sqlalchemy.orm import sessionmaker, Session  # Session management
from sqlalchemy.pool import StaticPool  # Connection pooling

# Application imports
from app.db.database import Base, get_db  # Database models and dependencies
from app.main import app  # FastAPI application


# Configure the test database
# Use in-memory SQLite for tests (":memory:" equivalent)
# This creates a new database for each test session that exists only in memory
SQLALCHEMY_DATABASE_URL: str = "sqlite://"

# Create a SQLAlchemy engine for the test database
engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # Use the in-memory SQLite URL
    connect_args={"check_same_thread": False},  # Allow SQLite to be used with multiple threads
    poolclass=StaticPool,  # Use a static connection pool to keep connections alive
)

# Create a sessionmaker for test database sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Pytest fixture that provides a SQLAlchemy session for testing.

    This fixture:
    1. Creates all database tables before each test
    2. Provides a database session for the test
    3. Closes the session after the test
    4. Drops all tables after the test

    The "function" scope ensures each test gets a fresh database.

    Yields:
        A SQLAlchemy Session connected to the test database
    """
    # Create all tables defined in the models
    Base.metadata.create_all(bind=engine)

    # Create a new database session for the test
    db: Session = TestingSessionLocal()
    try:
        # Provide the session to the test
        yield db
    finally:
        # Ensure the session is closed even if the test fails
        db.close()

    # Drop all tables after the test to start fresh for the next test
    # This ensures test isolation - no data leaks between tests
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Pytest fixture that provides a FastAPI TestClient for testing API endpoints.

    This fixture:
    1. Overrides the database dependency to use the test database
    2. Creates a FastAPI test client
    3. Resets the dependency override after the test

    The fixture depends on the 'db' fixture to ensure the test database is set up.

    Args:
        db: The test database session (injected by pytest)

    Yields:
        A FastAPI TestClient configured to use the test database
    """
    # Define a function to override the get_db dependency
    # This ensures API calls use our test database instead of the real one
    def override_get_db() -> Generator[Session, None, None]:
        try:
            yield db
        finally:
            db.close()

    # Override the dependency in the FastAPI app
    app.dependency_overrides[get_db] = override_get_db

    # Create and yield a test client
    with TestClient(app) as c:
        yield c

    # Reset the dependency overrides after the test
    # This prevents side effects between tests
    app.dependency_overrides = {}