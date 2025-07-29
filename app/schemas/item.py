"""
Pydantic schemas for Item model.

This module defines Pydantic models (schemas) for the Item entity.
These schemas are used for data validation, serialization, and documentation.

The schemas follow a pattern:
- Base schema with shared properties
- Create schema for item creation
- Update schema for item updates
- DB schema for items as stored in the database
- Response schema for items returned to clients
"""

from typing import Optional  # For optional fields
from datetime import datetime  # For timestamp fields
from pydantic import BaseModel  # Base Pydantic model


class ItemBase(BaseModel):
    """
    Base Pydantic schema for Item with shared properties.

    This defines the common attributes that are present in all item schemas.
    It serves as the foundation for other item-related schemas.

    Attributes:
        name: The name of the item
        description: A detailed description of the item (optional)
        is_active: Flag indicating if the item is active
    """
    name: str  # Required field
    description: Optional[str] = None  # Optional field with default None
    is_active: bool = True  # Optional field with default True


class ItemCreate(ItemBase):
    """
    Schema for creating a new Item.

    This schema is used when receiving data from clients to create a new item.
    It inherits all fields from ItemBase with no additional fields.

    In this case, all fields from ItemBase are required for item creation,
    except those with default values.
    """
    pass  # No additional fields required for item creation


class ItemUpdate(BaseModel):
    """
    Schema for updating an existing Item.

    This schema is used when receiving data from clients to update an existing item.
    It makes all fields optional, as updates may only include a subset of fields.

    Attributes:
        name: The name of the item (optional for updates)
        description: A detailed description of the item (optional)
        is_active: Flag indicating if the item is active (optional for updates)
    """
    name: Optional[str] = None  # Optional for updates
    description: Optional[str] = None  # Optional field with default None
    is_active: Optional[bool] = None  # Optional for updates


class ItemInDBBase(ItemBase):
    """
    Base schema for Item as stored in the database.

    This schema extends ItemBase with additional fields that are
    present in the database model but not in the input schemas.

    Attributes:
        id: The unique identifier for the item
        created_at: Timestamp when the item was created
        updated_at: Timestamp when the item was last updated
    """
    id: int  # Database-assigned ID
    created_at: datetime  # Creation timestamp
    updated_at: datetime  # Last update timestamp

    class Config:
        """
        Pydantic configuration for the schema.
        """
        orm_mode = True  # Enables ORM mode for converting SQLAlchemy models to Pydantic models


class Item(ItemInDBBase):
    """Schema for Item responses returned to clients."""
    pass  # Uses all fields from ItemInDBBase


class ItemInDB(ItemInDBBase):
    """
    Schema representing the Item as stored in the database.

    Used for internal operations that require the exact database representation.
    """
    pass  # Currently identical to ItemInDBBase, but could be extended
