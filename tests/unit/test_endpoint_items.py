from fastapi.testclient import TestClient

# pytest will automatically discover and inject the 'client' fixture from conftest.py
# client = TestClient(app) # No longer needed here


def test_create_and_get_item(client: TestClient):
    """
    Test creating a new item and then retrieving it.
    """
    # 1. Define the item to be created
    item_data = {"name": "Test Item", "description": "A sample item for testing."}
    headers = {"Content-Type": "application/json"}

    # 2. Send a POST request to create the item
    create_response = client.post("/items/", json=item_data, headers=headers)

    # 3. Assert the creation was successful
    assert create_response.status_code == 201
    created_item = create_response.json()
    assert "id" in created_item
    assert created_item["name"] == item_data["name"]
    assert created_item["description"] == item_data["description"]

    # 4. Get the ID of the newly created item
    item_id = created_item["id"]

    # 5. Send a GET request to retrieve the item by its ID
    get_response = client.get(f"/items/{item_id}")

    # 6. Assert the retrieval was successful and data matches
    assert get_response.status_code == 200
    retrieved_item = get_response.json()
    assert retrieved_item["id"] == item_id
    assert retrieved_item["name"] == item_data["name"]
    assert retrieved_item["description"] == item_data["description"]


def test_get_item_not_found(client: TestClient):
    """
    Test retrieving an item that does not exist.
    """
    # Request an item with an ID that is unlikely to exist
    non_existent_id = 99999
    response = client.get(f"/items/{non_existent_id}")

    # Assert that the response is a 404 Not Found
    assert response.status_code == 404
    assert response.json() == {"detail": f"Item with ID {non_existent_id} not found."}


def test_create_item_invalid_payload(client: TestClient):
    """
    Test creating an item with an invalid payload (e.g., missing required field).
    """
    # Payload is missing the required 'name' field
    invalid_data = {"description": "This item is missing a name.", "priority": 0}
    headers = {"Content-Type": "application/json"}

    response = client.post("/items/", json=invalid_data, headers=headers)

    # Assert that the response is a 422 Unprocessable Entity
    assert response.status_code == 422
