"""
Base model module for SQLAlchemy models.

This module defines a base class that all SQLAlchemy models will inherit from,
providing common functionality and columns that should be present in all tables.
"""

from datetime import datetime  # For timestamp fields
from typing import Any  # For type annotations

# SQLAlchemy imports
from sqlalchemy import Column, DateTime, Integer  # Column types
from sqlalchemy.ext.declarative import as_declarative, declared_attr  # Declarative base functionality


@as_declarative()
class Base:
    """
    Base class for all SQLAlchemy models.

    This class provides:
    1. Automatic table name generation based on the class name
    2. Common columns (id, created_at, updated_at) for all models
    3. A foundation for type annotations

    All model classes should inherit from this base class to ensure
    consistent structure and behavior across the application's data models.
    """
    # Type annotations for static type checking
    id: Any  # Primary key field
    __name__: str  # Class name, used for generating table name

    # Generate __tablename__ automatically based on the class name
    @declared_attr
    def __tablename__(cls) -> str:
        """
        Automatically generates the table name from the class name.

        This converts the CamelCase class name to lowercase for use as the table name.
        For example, a class named 'UserProfile' would use table name 'userprofile'.

        Returns:
            The lowercase version of the class name as the table name
        """
        return cls.__name__.lower()

    # Common columns that will be included in all model tables

    # Primary key column
    id = Column(
        Integer, 
        primary_key=True,  # Designates this column as the primary key
        index=True  # Creates an index on this column for faster lookups
    )

    # Creation timestamp
    created_at = Column(
        DateTime,  # Date and time type
        default=datetime.utcnow,  # Automatically set to current UTC time on creation
        nullable=False  # This column cannot be NULL
    )

    # Last update timestamp
    updated_at = Column(
        DateTime,  # Date and time type
        default=datetime.utcnow,  # Default value when record is created
        onupdate=datetime.utcnow,  # Automatically updated when record is modified
        nullable=False  # This column cannot be NULL
    )
