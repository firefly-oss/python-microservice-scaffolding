"""
REST Client module for making HTTP requests with httpx and Pydantic.

This module provides a RestClient class that can be used to make HTTP requests
to external services. It uses httpx for HTTP requests and Pydantic for data
validation and serialization/deserialization.

Example:
    ```python
    from app.core.rest_client import RestClient
    from pydantic import BaseModel

    class User(BaseModel):
        id: int
        name: str
        email: str

    # Create a client for a specific API
    client = RestClient(base_url="https://api.example.com")

    # Get a single user
    user = client.get("/users/1", response_model=User)
    print(user.name)

    # Get a list of users
    users = client.get("/users", response_model=list[User])
    for user in users:
        print(user.email)

    # Create a new user
    new_user = User(id=0, name="John Doe", email="john@example.com")
    created_user = client.post("/users", json=new_user, response_model=User)
    ```
"""
from typing import Any, Dict, Optional, Type, TypeVar, Union
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel

from app.core.logging import get_logger

# Type variable for Pydantic models
T = TypeVar("T", bound=BaseModel)
ResponseType = TypeVar("ResponseType")

logger = get_logger(__name__)


class RestClientError(Exception):
    """Base exception for REST client errors."""

    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[httpx.Response] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class RestClient:
    """
    A client for making HTTP requests to external services.

    This client uses httpx for HTTP requests and Pydantic for data validation
    and serialization/deserialization.

    Attributes:
        base_url: The base URL for the API.
        timeout: The timeout for requests in seconds.
        headers: Default headers to include in all requests.
        client: The httpx client instance.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[httpx.Auth] = None,
        verify: bool = True,
        retries: int = 3,
    ):
        """
        Initialize the REST client.

        Args:
            base_url: The base URL for the API.
            timeout: The timeout for requests in seconds.
            headers: Default headers to include in all requests.
            auth: Authentication to use for requests.
            verify: Whether to verify SSL certificates.
            retries: Number of times to retry failed requests.
        """
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers or {}
        self.auth = auth
        self.verify = verify
        self.retries = retries

        # Log a warning if SSL verification is disabled
        if not verify:
            logger.warning(
                "SSL verification is disabled. This is a security risk in production."
            )

        # Set up default headers
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "application/json"
        if "Accept" not in self.headers:
            self.headers["Accept"] = "application/json"

        # Create the client with a transport that retries
        transport = httpx.HTTPTransport(retries=retries)
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
            auth=self.auth,
            verify=self.verify,
            transport=transport,
        )

    def __del__(self):
        """Close the client when the object is deleted."""
        if hasattr(self, "client"):
            self.client.close()

    def _build_url(self, path: str) -> str:
        """
        Build the full URL from the base URL and path.

        Args:
            path: The path to append to the base URL.

        Returns:
            The full URL.
        """
        return urljoin(self.base_url, path)

    def _handle_response(
        self, response: httpx.Response, response_model: Optional[Type[ResponseType]] = None
    ) -> Union[httpx.Response, None, ResponseType]:
        """
        Handle the response from an HTTP request.

        Args:
            response: The HTTP response.
            response_model: The Pydantic model to parse the response into.

        Returns:
            The parsed response data.

        Raises:
            RestClientError: If the response contains an error.
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP error",
                status_code=e.response.status_code,
                url=str(e.response.url),
                response_text=e.response.text,
            )
            raise RestClientError(
                f"HTTP error: {e.response.status_code} {e.response.reason_phrase}",
                status_code=e.response.status_code,
                response=e.response,
            ) from e

        # If no response model is provided, return the raw response
        if response_model is None:
            return response

        # If the response is empty, return None
        if not response.content:
            return None

        try:
            # Parse the response into the provided model
            data = response.json()

            # Handle list responses
            if isinstance(data, list) and getattr(response_model, "__origin__", None) is list:
                item_model = response_model.__args__[0]  # type: ignore
                return [item_model.parse_obj(item) for item in data]

            # Handle single object responses
            return response_model.parse_obj(data)  # type: ignore
        except Exception as e:
            logger.error(
                "Failed to parse response",
                error=str(e),
                response_text=response.text,
            )
            raise RestClientError(f"Failed to parse response: {str(e)}") from e

    def request(
        self,
        method: str,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make an HTTP request.

        Args:
            method: The HTTP method to use.
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.

        Raises:
            RestClientError: If the request fails.
        """
        url = self._build_url(path)

        # Handle Pydantic models in the request body
        if "json" in kwargs and isinstance(kwargs["json"], BaseModel):
            kwargs["json"] = kwargs["json"].dict(exclude_unset=True)

        try:
            logger.debug(f"Making {method} request to {url}")
            response = self.client.request(method, url, **kwargs)
            return self._handle_response(response, response_model)
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise RestClientError(f"Request error: {str(e)}") from e

    def get(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a GET request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return self.request("GET", path, response_model, **kwargs)

    def post(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a POST request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return self.request("POST", path, response_model, **kwargs)

    def put(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a PUT request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return self.request("PUT", path, response_model, **kwargs)

    def patch(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a PATCH request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return self.request("PATCH", path, response_model, **kwargs)

    def delete(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a DELETE request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return self.request("DELETE", path, response_model, **kwargs)


class AsyncRestClient:
    """
    An asynchronous client for making HTTP requests to external services.

    This client uses httpx for HTTP requests and Pydantic for data validation
    and serialization/deserialization.

    Attributes:
        base_url: The base URL for the API.
        timeout: The timeout for requests in seconds.
        headers: Default headers to include in all requests.
        client: The httpx client instance.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 10.0,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[httpx.Auth] = None,
        verify: bool = True,
        retries: int = 3,
    ):
        """
        Initialize the async REST client.

        Args:
            base_url: The base URL for the API.
            timeout: The timeout for requests in seconds.
            headers: Default headers to include in all requests.
            auth: Authentication to use for requests.
            verify: Whether to verify SSL certificates.
            retries: Number of times to retry failed requests.
        """
        self.base_url = base_url
        self.timeout = timeout
        self.headers = headers or {}
        self.auth = auth
        self.verify = verify
        self.retries = retries

        # Log a warning if SSL verification is disabled
        if not verify:
            logger.warning(
                "SSL verification is disabled. This is a security risk in production."
            )

        # Set up default headers
        if "Content-Type" not in self.headers:
            self.headers["Content-Type"] = "application/json"
        if "Accept" not in self.headers:
            self.headers["Accept"] = "application/json"

        # Create the client with a transport that retries
        transport = httpx.AsyncHTTPTransport(retries=retries)
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
            auth=self.auth,
            verify=self.verify,
            transport=transport,
        )

    async def __aenter__(self) -> "AsyncRestClient":
        """Enter the async context manager."""
        return self

    async def __aexit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        """Exit the async context manager."""
        await self.close()

    async def close(self) -> None:
        """Close the client."""
        if hasattr(self, "client"):
            await self.client.aclose()

    def _build_url(self, path: str) -> str:
        """
        Build the full URL from the base URL and path.

        Args:
            path: The path to append to the base URL.

        Returns:
            The full URL.
        """
        return urljoin(self.base_url, path)

    async def _handle_response(
        self, response: httpx.Response, response_model: Optional[Type[ResponseType]] = None
    ) -> Union[httpx.Response, None, ResponseType]:
        """
        Handle the response from an HTTP request.

        Args:
            response: The HTTP response.
            response_model: The Pydantic model to parse the response into.

        Returns:
            The parsed response data.

        Raises:
            RestClientError: If the response contains an error.
        """
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP error",
                status_code=e.response.status_code,
                url=str(e.response.url),
                response_text=e.response.text,
            )
            raise RestClientError(
                f"HTTP error: {e.response.status_code} {e.response.reason_phrase}",
                status_code=e.response.status_code,
                response=e.response,
            ) from e

        # If no response model is provided, return the raw response
        if response_model is None:
            return response

        # If the response is empty, return None
        if not response.content:
            return None

        try:
            # Parse the response into the provided model
            data = response.json()

            # Handle list responses
            if isinstance(data, list) and getattr(response_model, "__origin__", None) is list:
                item_model = response_model.__args__[0]  # type: ignore
                return [item_model.parse_obj(item) for item in data]

            # Handle single object responses
            return response_model.parse_obj(data)  # type: ignore
        except Exception as e:
            logger.error(
                "Failed to parse response",
                error=str(e),
                response_text=response.text,
            )
            raise RestClientError(f"Failed to parse response: {str(e)}") from e

    async def request(
        self,
        method: str,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make an HTTP request.

        Args:
            method: The HTTP method to use.
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.

        Raises:
            RestClientError: If the request fails.
        """
        url = self._build_url(path)

        # Handle Pydantic models in the request body
        if "json" in kwargs and isinstance(kwargs["json"], BaseModel):
            kwargs["json"] = kwargs["json"].dict(exclude_unset=True)

        try:
            logger.debug(f"Making {method} request to {url}")
            response = await self.client.request(method, url, **kwargs)
            return await self._handle_response(response, response_model)
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            raise RestClientError(f"Request error: {str(e)}") from e

    async def get(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a GET request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return await self.request("GET", path, response_model, **kwargs)

    async def post(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a POST request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return await self.request("POST", path, response_model, **kwargs)

    async def put(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a PUT request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return await self.request("PUT", path, response_model, **kwargs)

    async def patch(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a PATCH request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return await self.request("PATCH", path, response_model, **kwargs)

    async def delete(
        self,
        path: str,
        response_model: Optional[Type[ResponseType]] = None,
        **kwargs: Any,
    ) -> Any:
        """
        Make a DELETE request.

        Args:
            path: The path to request.
            response_model: The Pydantic model to parse the response into.
            **kwargs: Additional arguments to pass to httpx.

        Returns:
            The parsed response data.
        """
        return await self.request("DELETE", path, response_model, **kwargs)
