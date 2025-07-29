"""
Item service module.

This module provides service functions for item operations, serving as an
intermediary between API endpoints and repository operations. It encapsulates
the business logic related to items.
"""

from typing import List, Optional, Dict, Any, Union, Tuple  # Type hints

from sqlalchemy.orm import Session  # SQLAlchemy session for database operations

# Application imports
from app import models, schemas  # Models and schemas
from app import repositories  # Repository operations


def get_items(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    with_pagination: bool = False,
    filters: Optional[Dict[str, Any]] = None
) -> Union[List[models.Item], Tuple[List[models.Item], Dict[str, Any]]]:
    """
    Get multiple items with pagination and optional filtering.

    Args:
        db: Database session
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return (for pagination)
        with_pagination: If True, returns pagination metadata along with results
        filters: Optional dictionary of field names and values to filter by

    Returns:
        If with_pagination is False: List of items
        If with_pagination is True: Tuple containing (list of items, pagination metadata)
    """
    if filters:
        return repositories.item.filter(
            db, filters=filters, skip=skip, limit=limit, with_pagination=with_pagination
        )
    return repositories.item.get_multi(
        db, skip=skip, limit=limit, with_pagination=with_pagination
    )


def create_item(db: Session, item_in: schemas.ItemCreate) -> models.Item:
    """
    Create a new item.

    Args:
        db: Database session
        item_in: Item data for creation

    Returns:
        The created item
    """
    return repositories.item.create(db=db, obj_in=item_in)


def get_item(db: Session, id: int) -> Optional[models.Item]:
    """
    Get a specific item by ID.

    Args:
        db: Database session
        id: The ID of the item to retrieve

    Returns:
        The requested item or None if not found
    """
    return repositories.item.get(db=db, id=id)


def update_item(
    db: Session, id: int, item_in: schemas.ItemUpdate
) -> Optional[models.Item]:
    """
    Update an existing item.

    Args:
        db: Database session
        id: The ID of the item to update
        item_in: Item update data

    Returns:
        The updated item or None if not found
    """
    item = repositories.item.get(db=db, id=id)
    if not item:
        return None
    return repositories.item.update(db=db, db_obj=item, obj_in=item_in)


def delete_item(db: Session, id: int) -> Optional[models.Item]:
    """
    Delete an item.

    Args:
        db: Database session
        id: The ID of the item to delete

    Returns:
        The deleted item or None if not found
    """
    item = repositories.item.get(db=db, id=id)
    if not item:
        return None
    return repositories.item.remove(db=db, id=id)
