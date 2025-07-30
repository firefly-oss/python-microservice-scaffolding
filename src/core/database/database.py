import os
from typing import Generator

from sqlmodel import create_engine, Session, SQLModel

import logging
from src.utils.logging import configure_logging

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Configure logging
configure_logging()
logger = logging.getLogger(__name__)

_engine = None


def get_engine():
    global _engine
    if _engine is None:
        logger.info(f"Initializing database engine with URL: {DATABASE_URL}")
        _engine = create_engine(DATABASE_URL, echo=True)
    return _engine


def create_db_and_tables(eng=None):
    """
    Creates all database tables defined by SQLModel metadata.
    This function is typically used for initial setup or testing.
    """
    if eng is None:
        eng = get_engine()
    SQLModel.metadata.create_all(eng)


def drop_db_and_tables(eng=None):
    """
    Drops all database tables defined by SQLModel metadata.
    This function is typically used for cleaning up test environments.
    """
    if eng is None:
        eng = get_engine()
    SQLModel.metadata.drop_all(eng)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Yields:
        Session: A SQLAlchemy session object.
    """
    with Session(get_engine()) as session:
        yield session
