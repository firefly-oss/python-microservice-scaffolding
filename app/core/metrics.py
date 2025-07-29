"""
Metrics configuration module for the application.

This module sets up Prometheus metrics for monitoring the application's
performance and behavior. It defines metrics for tracking HTTP requests,
response times, and application information, and provides middleware to
automatically record these metrics for each request.
"""

from prometheus_client import Counter, Histogram, Info  # Prometheus metric types
import time  # For measuring request duration
from typing import Callable  # Type hints

# FastAPI components
from fastapi import FastAPI, Request, Response
from prometheus_client import (
    REGISTRY, generate_latest  # Prometheus registry and output generation
)

# Define metrics
# Counter: A cumulative metric that represents a single monotonically increasing counter
REQUEST_COUNT: Counter = Counter(
    "http_requests_total",  # Metric name
    "Total number of HTTP requests",  # Metric description
    ["method", "endpoint", "status_code"]  # Labels for the metric
)

# Histogram: Samples observations and counts them in configurable buckets
# Used for measuring request duration with quantiles
REQUEST_LATENCY: Histogram = Histogram(
    "http_request_duration_seconds",  # Metric name
    "HTTP request latency in seconds",  # Metric description
    ["method", "endpoint"]  # Labels for the metric
)

# Info: A gauge with a constant '1' value labeled by arbitrary key-value pairs
# Used for exposing static information about the application
APP_INFO: Info = Info(
    "app_info",  # Metric name
    "Application information"  # Metric description
)


def setup_metrics(app: FastAPI, app_name: str, app_version: str) -> None:
    """
    Set up Prometheus metrics for the application.

    This function configures the application to expose Prometheus metrics
    and adds middleware to track request counts and latencies automatically.

    Args:
        app: FastAPI application instance to configure
        app_name: Name of the application for identification in metrics
        app_version: Version of the application for identification in metrics
    """
    # Set application info metric with name and version
    APP_INFO.info({"name": app_name, "version": app_version})

    # Add metrics endpoint to expose Prometheus metrics
    @app.get("/metrics")
    async def metrics() -> Response:
        """
        Endpoint that exposes Prometheus metrics.

        Returns:
            A plain text response containing all registered Prometheus metrics
        """
        return Response(
            content=generate_latest(REGISTRY),  # Generate metrics output from registry
            media_type="text/plain"  # Prometheus metrics are exposed as plain text
        )

    # Add middleware to automatically track request count and latency for all endpoints
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next: Callable) -> Response:
        """
        Middleware that records metrics for each HTTP request.

        Args:
            request: The incoming HTTP request
            call_next: Function to call the next middleware or route handler

        Returns:
            The HTTP response from the route handler
        """
        # Extract request information
        method: str = request.method  # HTTP method (GET, POST, etc.)
        path: str = request.url.path  # Request path

        # Exclude metrics endpoint from metrics to avoid recursion
        # (otherwise the metrics endpoint would record itself)
        if path == "/metrics":
            return await call_next(request)

        # Record start time to measure request duration
        start_time: float = time.time()

        # Process the request through the rest of the middleware chain and route handler
        response: Response = await call_next(request)

        # Record request latency in the histogram
        REQUEST_LATENCY.labels(
            method=method,
            endpoint=path
        ).observe(time.time() - start_time)  # Calculate and record duration

        # Increment request counter with method, path, and status code labels
        REQUEST_COUNT.labels(
            method=method,
            endpoint=path,
            status_code=response.status_code
        ).inc()  # Increment by 1

        return response
