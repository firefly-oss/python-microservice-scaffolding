"""
Base Repository (Create, Read, Update, Delete) operations module.

This module provides a generic base class for CRUD operations that can be
used with any SQLAlchemy model and Pydantic schema. It implements common
database operations to reduce code duplication across different models.
"""

from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union, Tuple  # Type hints

# FastAPI and Pydantic imports
from fastapi.encoders import jsonable_encoder  # For converting Pydantic models to JSON-compatible dict
from pydantic import BaseModel  # Base class for Pydantic schemas
from sqlalchemy.orm import Session  # SQLAlchemy session for database operations
from sqlalchemy import and_  # For combining filter conditions

# Application imports
from app.models.base import Base  # Base SQLAlchemy model

# Define generic type variables for type safety
ModelType = TypeVar("ModelType", bound=Base)  # SQLAlchemy model type
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # Pydantic schema for creation
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # Pydantic schema for updates


class CRUDRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base class for CRUD operations.

    This generic class provides standard Create, Read, Update, Delete operations
    that work with any SQLAlchemy model and corresponding Pydantic schemas.

    Type Parameters:
        ModelType: The SQLAlchemy model type
        CreateSchemaType: The Pydantic schema type for creation operations
        UpdateSchemaType: The Pydantic schema type for update operations
    """
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the Repository object with a specific SQLAlchemy model.

        Args:
            model: The SQLAlchemy model class this Repository object will operate on
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.

        Args:
            db: SQLAlchemy database session
            id: ID of the record to get

        Returns:
            The model instance if found, None otherwise
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100, with_pagination: bool = False
    ) -> Union[List[ModelType], Tuple[List[ModelType], Dict[str, Any]]]:
        """
        Get multiple records with pagination.

        Args:
            db: SQLAlchemy database session
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            with_pagination: If True, returns pagination metadata along with results

        Returns:
            If with_pagination is False: List of model instances
            If with_pagination is True: Tuple containing (list of model instances, pagination metadata)
        """
        query = db.query(self.model)

        # Get total count for pagination metadata
        if with_pagination:
            total = query.count()

        # Apply pagination
        items = query.offset(skip).limit(limit).all()

        # Return with pagination metadata if requested
        if with_pagination:
            pagination = {
                "total": total,
                "skip": skip,
                "limit": limit,
                "has_more": (total > skip + limit)
            }
            return items, pagination

        return items

    def filter(
        self, db: Session, *, filters: Dict[str, Any], skip: int = 0, 
        limit: int = 100, with_pagination: bool = False
    ) -> Union[List[ModelType], Tuple[List[ModelType], Dict[str, Any]]]:
        """
        Filter records based on field values with pagination.

        Args:
            db: SQLAlchemy database session
            filters: Dictionary of field names and values to filter by
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return
            with_pagination: If True, returns pagination metadata along with results

        Returns:
            If with_pagination is False: List of model instances matching the filters
            If with_pagination is True: Tuple containing (list of model instances, pagination metadata)
        """
        query = db.query(self.model)

        # Apply filters
        filter_conditions = []
        for field, value in filters.items():
            if hasattr(self.model, field):
                filter_conditions.append(getattr(self.model, field) == value)

        if filter_conditions:
            query = query.filter(and_(*filter_conditions))

        # Get total count for pagination metadata
        if with_pagination:
            total = query.count()

        # Apply pagination
        items = query.offset(skip).limit(limit).all()

        # Return with pagination metadata if requested
        if with_pagination:
            pagination = {
                "total": total,
                "skip": skip,
                "limit": limit,
                "has_more": (total > skip + limit)
            }
            return items, pagination

        return items

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Args:
            db: SQLAlchemy database session
            obj_in: Pydantic schema with the data to create

        Returns:
            The created model instance
        """
        # Convert Pydantic model to dict
        obj_in_data = jsonable_encoder(obj_in)

        # Create SQLAlchemy model instance with the data
        db_obj = self.model(**obj_in_data)

        # Add to session, commit, and refresh to get the ID and any default values
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update an existing record.

        Args:
            db: SQLAlchemy database session
            db_obj: SQLAlchemy model instance to update
            obj_in: Pydantic schema or dict with the update data

        Returns:
            The updated model instance
        """
        # Convert current object to dict
        obj_data = jsonable_encoder(db_obj)

        # Prepare update data based on input type
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            # Convert Pydantic model to dict, excluding unset fields
            update_data = obj_in.dict(exclude_unset=True)

        # Update only the fields that are present in the input
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        # Save changes to database
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Delete a record by ID.

        Args:
            db: SQLAlchemy database session
            id: ID of the record to delete

        Returns:
            The deleted model instance
        """
        # Get the object
        obj = db.query(self.model).get(id)

        # Delete it and commit
        db.delete(obj)
        db.commit()

        return obj
