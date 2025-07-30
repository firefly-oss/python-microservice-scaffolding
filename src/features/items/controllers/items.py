# src/features/items/controllers/items.py
# =======================================================================
# 📝 FILE OVERVIEW
# =======================================================================
"""
This module defines the API endpoints for the generic 'items' service.

It provides routes for creating and retrieving items, serving as a
reference for building new service endpoints.
"""

# =======================================================================
# ⚙️ 1. IMPORTS
# =======================================================================
import logging
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session  # Import Session
from ..models.items import ItemCreate, ItemRead  # Import ItemRead
from ..services import items as items_service
from src.core.database.database import get_session  # Import get_session

logger = logging.getLogger(__name__)

# =======================================================================
# 🚀 2. API ROUTER CONFIGURATION
# =======================================================================
router = APIRouter(
    tags=["Items"],
)


# =======================================================================
# 🔗 3. API ENDPOINTS
# =======================================================================


@router.post(
    "/items", response_model=ItemRead, status_code=status.HTTP_201_CREATED
)  # Changed response_model to ItemRead
def create_new_item(item_in: ItemCreate, session: Session = Depends(get_session)):
    """
    API endpoint to create a new item.

    Receives item data in the request body, passes it to the controller,
    and returns the created item.
    """
    logger.info("Received request to create a new item.")
    try:
        created_item = items_service.create_item(item_in, session)  # Pass session to controller
        return created_item
    except Exception as e:
        logger.error(f"An unexpected error occurred while creating an item: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while creating the item.",
        )


@router.get("/items/{item_id}", response_model=ItemRead)  # Changed response_model to ItemRead
def get_single_item(item_id: int, session: Session = Depends(get_session)):
    """
    API endpoint to retrieve a single item by its ID.
    """
    logger.info(f"Received request to get item with ID: {item_id}")
    try:
        item = items_service.get_item(item_id, session)  # Pass session to controller
        if item is None:
            logger.warning(f"Item with ID {item_id} not found in router.")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item with ID {item_id} not found.",
            )
        return item
    except HTTPException:
        # Re-raise HTTPException to preserve the original status code and detail
        raise
    except Exception as e:
        logger.error(f"An unexpected error occurred while retrieving item {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while retrieving the item.",
        )


@router.get("/items", response_model=List[ItemRead])
def get_all_items(session: Session = Depends(get_session)):
    """
    API endpoint to retrieve all items.
    """
    logger.info("Received request to get all items.")
    try:
        items = items_service.get_all_items(session)
        return items
    except Exception as e:
        logger.error(f"An unexpected error occurred while retrieving all items: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred while retrieving all items.",
        )
