import pytest
from fastapi.testclient import TestClient
from src.fastapi.api_handler import app

client = TestClient(app)


@pytest.mark.parametrize(
    "headers, expected_status_code, expected_response",
    [
        (
            {"x-api-key": "dummy-key"},  # simulate an API key if required
            200,
            {"status": "ok"},  # Partial check; version may vary dynamically
        ),
        (
            {},  # No headers
            200,  # Adjust this if your endpoint requires auth
            {"status": "ok"},
        ),
    ],
)
def test_health_endpoint(headers, expected_status_code, expected_response):
    """
    Test the /health endpoint for correct status and partial response fields.
    """
    response = client.get("/health", headers=headers)

    assert response.status_code == expected_status_code
    json_data = response.json()

    assert json_data["status"] == expected_response["status"]
    assert "version" in json_data  # Optional: Check version presence
    assert isinstance(json_data["version"], str)
