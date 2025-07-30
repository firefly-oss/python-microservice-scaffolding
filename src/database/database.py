from typing import Generator

from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = "sqlite:///./sql_app.db"

# SQLite engine for development
# For PostgreSQL, it would be:
# postgres_url = "postgresql://user:password@host:port/database"
# engine = create_engine(postgres_url)

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """
    Creates all database tables defined by SQLModel metadata.
    This function is typically used for initial setup or testing.
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency that provides a database session.

    Yields:
        Session: A SQLAlchemy session object.
    """
    with Session(engine) as session:
        yield session
