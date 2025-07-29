"""
Tests for the items API endpoints.

This module contains tests for all CRUD operations on items:
- Creating items
- Reading individual items
- Reading lists of items
- Updating items
- Deleting items

These tests use pytest fixtures defined in tests/conftest.py for
the test client and database session.
"""

from fastapi.testclient import TestClient  # FastAPI test client
from sqlalchemy.orm import Session  # SQLAlchemy session for database operations

# Application imports
from app.services import item_service  # Item service functions
from app.schemas.item import ItemCreate  # Pydantic schema for item creation


def test_create_item(client: TestClient, db: Session) -> None:
    """
    Test creating a new item through the API.

    This test verifies that:
    1. The POST endpoint creates a new item
    2. The response contains the correct data
    3. The response includes required fields (id, timestamps)

    Args:
        client: FastAPI test client fixture
        db: SQLAlchemy database session fixture
    """
    # Prepare test data
    data = {"name": "Test Item", "description": "Test Description"}

    # Make POST request to create item
    response = client.post(
        "/api/v1/items/", json=data,
    )

    # Verify response status code
    assert response.status_code == 200

    # Parse response JSON
    content = response.json()

    # Verify response data matches input data
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]

    # Verify required fields are present
    assert "id" in content
    assert "created_at" in content
    assert "updated_at" in content


def test_read_item(client: TestClient, db: Session) -> None:
    """
    Test retrieving a specific item by ID.

    This test verifies that:
    1. An item can be created in the database
    2. The GET endpoint returns the correct item
    3. The response contains the expected data

    Args:
        client: FastAPI test client fixture
        db: SQLAlchemy database session fixture
    """
    # Create an item directly in the database using the service layer
    item_in = ItemCreate(name="Test Item", description="Test Description")
    item = item_service.create_item(db=db, item_in=item_in)

    # Make GET request to retrieve the item
    response = client.get(f"/api/v1/items/{item.id}")

    # Verify response status code
    assert response.status_code == 200

    # Parse response JSON
    content = response.json()

    # Verify response data matches the created item
    assert content["name"] == item.name
    assert content["description"] == item.description
    assert content["id"] == item.id


def test_read_items(client: TestClient, db: Session) -> None:
    """
    Test retrieving a list of items.

    This test verifies that:
    1. Multiple items can be created in the database
    2. The GET endpoint returns a list containing those items

    Args:
        client: FastAPI test client fixture
        db: SQLAlchemy database session fixture
    """
    # Create multiple items directly in the database using the service layer
    item1_in = ItemCreate(name="Test Item 1", description="Test Description 1")
    item2_in = ItemCreate(name="Test Item 2", description="Test Description 2")
    item_service.create_item(db=db, item_in=item1_in)
    item_service.create_item(db=db, item_in=item2_in)

    # Make GET request to retrieve all items
    response = client.get("/api/v1/items/")

    # Verify response status code
    assert response.status_code == 200

    # Parse response JSON
    content = response.json()

    # Verify the response contains at least the items we created
    # Note: There might be other items in the database from previous tests
    assert len(content) >= 2


def test_read_items_with_pagination(client: TestClient, db: Session) -> None:
    """
    Test retrieving a list of items with pagination.

    This test verifies that:
    1. Multiple items can be created in the database
    2. The GET endpoint returns paginated results with metadata
    3. The pagination parameters (skip, limit) work correctly

    Args:
        client: FastAPI test client fixture
        db: SQLAlchemy database session fixture
    """
    # Create multiple items directly in the database using the service layer
    for i in range(5):
        item_in = ItemCreate(name=f"Pagination Test Item {i}", description=f"Description {i}")
        item_service.create_item(db=db, item_in=item_in)

    # Make GET request with pagination
    response = client.get("/api/v1/items/?skip=1&limit=2&with_pagination=true")

    # Verify response status code
    assert response.status_code == 200

    # Parse response JSON
    content = response.json()

    # Verify the response structure includes pagination metadata
    assert "items" in content
    assert "total" in content
    assert "skip" in content
    assert "limit" in content
    assert "has_more" in content

    # Verify pagination parameters were applied correctly
    assert content["skip"] == 1
    assert content["limit"] == 2
    assert len(content["items"]) <= 2  # Should not exceed the limit

    # Verify total count is at least the number we created
    assert content["total"] >= 5


def test_filter_items(client: TestClient, db: Session) -> None:
    """
    Test filtering items by field values.

    This test verifies that:
    1. Items with different field values can be created
    2. The GET endpoint can filter items by field values
    3. The filter returns only matching items

    Args:
        client: FastAPI test client fixture
        db: SQLAlchemy database session fixture
    """
    # Create items with different is_active values
    item1_in = ItemCreate(name="Active Item", description="This item is active", is_active=True)
    item2_in = ItemCreate(name="Inactive Item", description="This item is inactive", is_active=False)
    item_service.create_item(db=db, item_in=item1_in)
    item_service.create_item(db=db, item_in=item2_in)

    # Make GET request with filter for active items
    response = client.get("/api/v1/items/?is_active=true")

    # Verify response status code
    assert response.status_code == 200

    # Parse response JSON
    content = response.json()

    # Verify all returned items are active
    for item in content:
        assert item["is_active"] is True

    # Make GET request with filter for inactive items
    response = client.get("/api/v1/items/?is_active=false")

    # Verify response status code
    assert response.status_code == 200

    # Parse response JSON
    content = response.json()

    # Verify all returned items are inactive
    for item in content:
        assert item["is_active"] is False


def test_update_item(client: TestClient, db: Session) -> None:
    """
    Test updating an existing item.

    This test verifies that:
    1. An item can be created in the database
    2. The PUT endpoint updates the item
    3. The response contains the updated data

    Args:
        client: FastAPI test client fixture
        db: SQLAlchemy database session fixture
    """
    # Create an item directly in the database using the service layer
    item_in = ItemCreate(name="Test Item", description="Test Description")
    item = item_service.create_item(db=db, item_in=item_in)

    # Prepare update data
    data = {"name": "Updated Item", "description": "Updated Description"}

    # Make PUT request to update the item
    response = client.put(f"/api/v1/items/{item.id}", json=data)

    # Verify response status code
    assert response.status_code == 200

    # Parse response JSON
    content = response.json()

    # Verify response data contains the updates
    assert content["name"] == data["name"]
    assert content["description"] == data["description"]
    assert content["id"] == item.id


def test_delete_item(client: TestClient, db: Session) -> None:
    """
    Test deleting an item.

    This test verifies that:
    1. An item can be created in the database
    2. The DELETE endpoint removes the item
    3. The item is no longer accessible after deletion

    Args:
        client: FastAPI test client fixture
        db: SQLAlchemy database session fixture
    """
    # Create an item directly in the database using the service layer
    item_in = ItemCreate(name="Test Item", description="Test Description")
    item = item_service.create_item(db=db, item_in=item_in)

    # Make DELETE request to remove the item
    response = client.delete(f"/api/v1/items/{item.id}")

    # Verify response status code
    assert response.status_code == 200

    # Verify the item is deleted by trying to retrieve it
    response = client.get(f"/api/v1/items/{item.id}")
    assert response.status_code == 404  # Should return Not Found
