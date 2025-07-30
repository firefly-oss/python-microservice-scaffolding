import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel

from src.fastapi.api_handler import app
from src.database.database import get_session, create_db_and_tables, drop_db_and_tables

# Use a separate database for testing
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://user:password@localhost:5432/test_db")

# Create a test engine for the module
test_engine = create_engine(TEST_DATABASE_URL, echo=True)

@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    with Session(test_engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()

def pytest_sessionstart(session):
    """
    Called once before the entire test session starts.
    """
    print(f"\nSetting up test database with URL: {TEST_DATABASE_URL}")
    drop_db_and_tables(test_engine)
    create_db_and_tables(test_engine)

def pytest_sessionfinish(session):
    """
    Called once after the entire test session finishes.
    """
    print("\nCleaning up test database.")
    drop_db_and_tables(test_engine)
