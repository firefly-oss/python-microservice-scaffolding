"""
Tests for the REST client module.
"""
import json
from typing import AsyncGenerator, Generator, List
from unittest.mock import MagicMock, patch

import httpx
import pytest
from pydantic import BaseModel

from app.core.rest_client import RestClient, RestClientError, AsyncRestClient


class User(BaseModel):
    """Test user model for REST client tests."""
    id: int
    name: str
    email: str


class TestRestClient:
    """Tests for the synchronous REST client."""

    @pytest.fixture
    def mock_response(self) -> MagicMock:
        """Create a mock response."""
        response = MagicMock(spec=httpx.Response)
        response.status_code = 200
        response.raise_for_status = MagicMock()
        return response

    @pytest.fixture
    def client(self) -> Generator[RestClient, None, None]:
        """Create a REST client for testing."""
        with patch("httpx.Client") as mock_client:
            client = RestClient(base_url="https://api.example.com")
            # Replace the real client with a mock
            client.client = mock_client
            yield client

    def test_get_request(self, client: RestClient, mock_response: MagicMock) -> None:
        """Test making a GET request."""
        # Set up the mock response
        user_data = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        mock_response.json.return_value = user_data
        mock_response.content = json.dumps(user_data).encode()
        client.client.request.return_value = mock_response

        # Make the request
        user = client.get("/users/1", response_model=User)

        # Check that the request was made correctly
        client.client.request.assert_called_once_with(
            "GET", "https://api.example.com/users/1"
        )

        # Check that the response was parsed correctly
        assert isinstance(user, User)
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    def test_get_list_request(self, client: RestClient, mock_response: MagicMock) -> None:
        """Test making a GET request that returns a list."""
        # Set up the mock response
        users_data = [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
        ]
        mock_response.json.return_value = users_data
        mock_response.content = json.dumps(users_data).encode()
        client.client.request.return_value = mock_response

        # Make the request
        users = client.get("/users", response_model=List[User])

        # Check that the request was made correctly
        client.client.request.assert_called_once_with(
            "GET", "https://api.example.com/users"
        )

        # Check that the response was parsed correctly
        assert isinstance(users, list)
        assert len(users) == 2
        assert all(isinstance(user, User) for user in users)
        assert users[0].id == 1
        assert users[0].name == "John Doe"
        assert users[1].id == 2
        assert users[1].name == "Jane Smith"

    def test_post_request(self, client: RestClient, mock_response: MagicMock) -> None:
        """Test making a POST request."""
        # Set up the mock response
        user_data = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        mock_response.json.return_value = user_data
        mock_response.content = json.dumps(user_data).encode()
        client.client.request.return_value = mock_response

        # Create a user to send
        new_user = User(id=0, name="John Doe", email="john@example.com")

        # Make the request
        user = client.post("/users", json=new_user, response_model=User)

        # Check that the request was made correctly
        client.client.request.assert_called_once_with(
            "POST", 
            "https://api.example.com/users", 
            json={"id": 0, "name": "John Doe", "email": "john@example.com"}
        )

        # Check that the response was parsed correctly
        assert isinstance(user, User)
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    def test_error_handling(self, client: RestClient) -> None:
        """Test handling HTTP errors."""
        # Set up a mock response with an error
        error_response = MagicMock(spec=httpx.Response)
        error_response.status_code = 404
        error_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not found", request=MagicMock(), response=error_response
        )
        error_response.url = "https://api.example.com/users/999"
        error_response.text = "Not found"
        error_response.reason_phrase = "Not Found"
        client.client.request.return_value = error_response

        # Make the request and check that it raises an error
        with pytest.raises(RestClientError) as excinfo:
            client.get("/users/999", response_model=User)

        # Check the error details
        assert "HTTP error: 404 Not Found" in str(excinfo.value)
        assert excinfo.value.status_code == 404
        assert excinfo.value.response == error_response


@pytest.mark.asyncio
class TestAsyncRestClient:
    """Tests for the asynchronous REST client."""

    @pytest.fixture
    async def mock_response(self) -> MagicMock:
        """Create a mock response."""
        response = MagicMock(spec=httpx.Response)
        response.status_code = 200
        response.raise_for_status = MagicMock()
        return response

    @pytest.fixture
    async def client(self) -> AsyncGenerator[AsyncRestClient, None]:
        """Create an async REST client for testing."""
        with patch("httpx.AsyncClient") as mock_client:
            client = AsyncRestClient(base_url="https://api.example.com")
            # Replace the real client with a mock
            client.client = mock_client
            yield client
            # Clean up
            await client.close()

    async def test_get_request(self, client: AsyncRestClient, mock_response: MagicMock) -> None:
        """Test making an async GET request."""
        # Set up the mock response
        user_data = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        mock_response.json.return_value = user_data
        mock_response.content = json.dumps(user_data).encode()
        client.client.request.return_value = mock_response

        # Make the request
        user = await client.get("/users/1", response_model=User)

        # Check that the request was made correctly
        client.client.request.assert_called_once_with(
            "GET", "https://api.example.com/users/1"
        )

        # Check that the response was parsed correctly
        assert isinstance(user, User)
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    async def test_post_request(self, client: AsyncRestClient, mock_response: MagicMock) -> None:
        """Test making an async POST request."""
        # Set up the mock response
        user_data = {"id": 1, "name": "John Doe", "email": "john@example.com"}
        mock_response.json.return_value = user_data
        mock_response.content = json.dumps(user_data).encode()
        client.client.request.return_value = mock_response

        # Create a user to send
        new_user = User(id=0, name="John Doe", email="john@example.com")

        # Make the request
        user = await client.post("/users", json=new_user, response_model=User)

        # Check that the request was made correctly
        client.client.request.assert_called_once_with(
            "POST", 
            "https://api.example.com/users", 
            json={"id": 0, "name": "John Doe", "email": "john@example.com"}
        )

        # Check that the response was parsed correctly
        assert isinstance(user, User)
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
