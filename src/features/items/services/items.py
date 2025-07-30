# src/features/items/services/items.py
# =======================================================================
# 📝 FILE OVERVIEW
# =======================================================================
"""
This module contains the business logic (services) for the items service.

It interacts with the database to perform CRUD operations on items.
"""

# =======================================================================
# ⚙️ 1. IMPORTS & CONFIGURATION
# =======================================================================
import logging
from typing import List, Optional
from sqlmodel import Session, select  # Import Session and select
from ..models.items import Item, ItemCreate  # ItemRead is not needed here, as we return Item objects

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =======================================================================
# 🚀 2. SERVICE FUNCTIONS
# =======================================================================
def create_item(item_in: ItemCreate, session: Session) -> Item:
    """
    Creates a new item and stores it in the database.

    Args:
        item_in: The item data from the request.
        session: The database session.

    Returns:
        The newly created item, including its server-generated ID.
    """
    logger.info(f"Creating new item with name: {item_in.name}")

    # Create a new Item instance from ItemCreate
    new_item = Item.model_validate(item_in)

    session.add(new_item)
    session.commit()
    session.refresh(new_item)  # Refresh to get the generated ID

    logger.info(f"Successfully created item with ID: {new_item.id}")
    return new_item


def get_item(item_id: int, session: Session) -> Optional[Item]:
    """
    Retrieves an item by its ID from the database.

    Args:
        item_id: The ID of the item to retrieve.
        session: The database session.

    Returns:
        The Item object if found, otherwise None.
    """
    logger.info(f"Attempting to retrieve item with ID: {item_id}")
    item = session.get(Item, item_id)

    if item:
        logger.info(f"Found item with ID: {item_id}")
    else:
        logger.warning(f"Item with ID {item_id} not found.")

    return item


def get_all_items(session: Session) -> List[Item]:
    """
    Retrieves all items from the database.

    Args:
        session: The database session.

    Returns:
        A list of all Item objects.
    """
    logger.info("Attempting to retrieve all items.")
    items = session.exec(select(Item)).all()
    logger.info(f"Found {len(items)} items.")
    return items
