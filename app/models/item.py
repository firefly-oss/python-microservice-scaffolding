"""
Item model module for the application.

This module defines the Item model which represents the 'item' table
in the database. It inherits from the Base model to get common fields
and functionality.
"""

from typing import Optional  # For optional field types

# SQLAlchemy imports
from sqlalchemy import Column, String, Boolean, Text  # Column types

# Import the base model class
from app.models.base import Base


class Item(Base):
    """
    Item model for storing item data in the database.

    This model inherits from the Base class, which provides:
    - id (Integer, primary key)
    - created_at (DateTime)
    - updated_at (DateTime)

    The Item model adds fields specific to items in the application.

    Attributes:
        name: The name of the item (required, indexed for faster searches)
        description: A detailed description of the item (optional)
        is_active: Flag indicating if the item is active (defaults to True)
    """
    # Item name - required, indexed for faster lookups
    name: str = Column(
        String(255),  # String type with maximum length of 255 characters
        nullable=False,  # This field cannot be NULL
        index=True  # Create an index on this column for faster searches
    )

    # Item description - optional
    description: Optional[str] = Column(
        Text,  # Text type for longer string content
        nullable=True  # This field can be NULL
    )

    # Active status flag
    is_active: bool = Column(
        Boolean,  # Boolean type (True/False)
        default=True  # Default value is True (active)
    )
