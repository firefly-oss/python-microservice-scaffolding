"""
API endpoints for item operations.

This module defines all the REST API endpoints for managing items,
including creating, reading, updating, and deleting items.
It uses the service layer to separate API handling from business logic.
"""

from typing import Any, List, Dict, Optional, Union  # Type hints

# FastAPI imports
from fastapi import APIRouter, Depends, HTTPException, Query  # API routing and dependencies
from pydantic import BaseModel  # For response models
from sqlalchemy.orm import Session  # Database session

# Application imports
from app import models, schemas  # Models and schemas
from app.db.database import get_db  # Database session dependency
from app.services import item_service  # Item service functions

# Create a router for item endpoints
router: APIRouter = APIRouter()


# Define a response model for paginated results
class PaginatedItems(BaseModel):
    items: List[schemas.Item]
    total: int
    skip: int
    limit: int
    has_more: bool

    class Config:
        orm_mode = True


@router.get("/", response_model=Union[List[schemas.Item], PaginatedItems])
def read_items(
    db: Session = Depends(get_db),  # Inject database session
    skip: int = 0,  # Pagination: number of items to skip
    limit: int = 100,  # Pagination: maximum number of items to return
    with_pagination: bool = False,  # Whether to include pagination metadata
    is_active: Optional[bool] = None,  # Filter by active status
) -> Any:
    """
    Retrieve a list of items with pagination and filtering.

    This endpoint returns a list of items from the database,
    with support for pagination and filtering.

    Args:
        db: Database session (injected by FastAPI)
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return (for pagination)
        with_pagination: If true, returns pagination metadata
        is_active: Filter by active status

    Returns:
        If with_pagination is False: List of items
        If with_pagination is True: Object containing items and pagination metadata

    Examples:
        GET /api/v1/items?skip=0&limit=10
        GET /api/v1/items?with_pagination=true
        GET /api/v1/items?is_active=true
        GET /api/v1/items?skip=0&limit=10&with_pagination=true&is_active=true
    """
    # Apply filters if provided
    filters = {}
    if is_active is not None:
        filters["is_active"] = is_active

    # Get items with pagination and/or filtering
    result = item_service.get_items(
        db, skip=skip, limit=limit, with_pagination=with_pagination, filters=filters
    )

    # Format response based on pagination flag
    if with_pagination:
        items, pagination = result
        return {
            "items": items,
            "total": pagination["total"],
            "skip": pagination["skip"],
            "limit": pagination["limit"],
            "has_more": pagination["has_more"]
        }
    return result


@router.post("/", response_model=schemas.Item)
def create_item(
    *,
    db: Session = Depends(get_db),  # Inject database session
    item_in: schemas.ItemCreate,  # Item data from request body
) -> Any:
    """
    Create a new item.

    This endpoint creates a new item in the database using the
    data provided in the request body.

    Args:
        db: Database session (injected by FastAPI)
        item_in: Item data from request body

    Returns:
        The created item

    Example:
        POST /api/v1/items
        {
            "name": "New Item",
            "description": "Description of the new item",
            "is_active": true
        }
    """
    # Create a new item using the service layer
    item = item_service.create_item(db=db, item_in=item_in)
    return item


@router.get("/{id}", response_model=schemas.Item)
def read_item(
    *,
    db: Session = Depends(get_db),  # Inject database session
    id: int,  # Item ID from path parameter
) -> Any:
    """
    Get a specific item by ID.

    This endpoint retrieves a single item from the database
    based on its ID.

    Args:
        db: Database session (injected by FastAPI)
        id: The ID of the item to retrieve (from URL path)

    Returns:
        The requested item

    Raises:
        HTTPException: If the item is not found (404)

    Example:
        GET /api/v1/items/123
    """
    # Get the item by ID using the service layer
    item = item_service.get_item(db=db, id=id)

    # Raise 404 if item not found
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.put("/{id}", response_model=schemas.Item)
def update_item(
    *,
    db: Session = Depends(get_db),  # Inject database session
    id: int,  # Item ID from path parameter
    item_in: schemas.ItemUpdate,  # Item update data from request body
) -> Any:
    """
    Update an existing item.

    This endpoint updates an existing item in the database
    using the data provided in the request body.

    Args:
        db: Database session (injected by FastAPI)
        id: The ID of the item to update (from URL path)
        item_in: Item update data from request body

    Returns:
        The updated item

    Raises:
        HTTPException: If the item is not found (404)

    Example:
        PUT /api/v1/items/123
        {
            "name": "Updated Item Name",
            "description": "Updated description"
        }
    """
    # Update the item using the service layer
    item = item_service.update_item(db=db, id=id, item_in=item_in)

    # Raise 404 if item not found
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.delete("/{id}", response_model=schemas.Item)
def delete_item(
    *,
    db: Session = Depends(get_db),  # Inject database session
    id: int,  # Item ID from path parameter
) -> Any:
    """
    Delete an item.

    This endpoint deletes an item from the database based on its ID.

    Args:
        db: Database session (injected by FastAPI)
        id: The ID of the item to delete (from URL path)

    Returns:
        The deleted item

    Raises:
        HTTPException: If the item is not found (404)

    Example:
        DELETE /api/v1/items/123
    """
    # Delete the item using the service layer
    item = item_service.delete_item(db=db, id=id)

    # Raise 404 if item not found
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item
