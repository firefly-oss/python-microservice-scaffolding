"""
API router configuration module for API v1.

This module sets up the main API router for version 1 of the API and
includes all the endpoint-specific routers. It serves as the central
point for organizing and structuring the API routes.
"""

from fastapi import APIRouter  # FastAPI router for organizing endpoints

# Import endpoint-specific routers
from app.api.api_v1.endpoints import items  # Router for item-related endpoints

# Create the main API router for version 1
api_router: APIRouter = APIRouter()

# Include all endpoint-specific routers with appropriate prefixes and tags
# The prefix adds a path segment before all routes in the included router
# The tags are used for grouping endpoints in the OpenAPI documentation
api_router.include_router(
    items.router,  # The router containing item-related endpoints
    prefix="/items",  # All item endpoints will be under /items
    tags=["items"]  # Group these endpoints under the "items" tag in docs
)

# Additional routers can be included here as the API grows
# For example:
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
