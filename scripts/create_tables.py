import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from src.services.items.models.items import Item  # Import your models here

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created.")


if __name__ == "__main__":
    create_db_and_tables()
