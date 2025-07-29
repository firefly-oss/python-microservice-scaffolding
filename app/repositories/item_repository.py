"""
Item-specific repository operations module.

This module extends the base repository operations for the Item model,
adding custom methods specific to Item entities.
"""

from typing import Optional  # For optional return types

from sqlalchemy.orm import Session  # SQLAlchemy session for database operations

# Import base repository class and model-specific components
from app.repositories.base import CRUDRepository  # Generic base repository class
from app.models.item import Item  # SQLAlchemy Item model
from app.schemas.item import ItemCreate, ItemUpdate  # Pydantic schemas for Item


class ItemRepository(CRUDRepository[Item, ItemCreate, ItemUpdate]):
    """
    Repository operations for Item model.

    This class extends the generic CRUDRepository class with Item-specific
    operations. It inherits all the standard CRUD methods (create,
    get, get_multi, update, remove) and adds custom methods for
    Item-specific queries.

    Type Parameters:
        Item: The SQLAlchemy Item model
        ItemCreate: The Pydantic schema for item creation
        ItemUpdate: The Pydantic schema for item updates
    """
    def get_by_name(self, db: Session, *, name: str) -> Optional[Item]:
        """
        Get an item by its name.

        This is a custom method specific to the Item model that allows
        retrieving items by their name field, which is a common lookup
        operation for items.

        Args:
            db: SQLAlchemy database session
            name: The name of the item to find

        Returns:
            The Item instance if found, None otherwise
        """
        return db.query(self.model).filter(self.model.name == name).first()


# Create a singleton instance of ItemRepository to be imported and used throughout the application
# This follows the repository pattern where this instance serves as the interface
# for all Item-related database operations
item: ItemRepository = ItemRepository(Item)