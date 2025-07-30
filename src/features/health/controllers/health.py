# src/features/health/controllers/health.py
# =======================================================================
# 📝 FILE OVERVIEW
# =======================================================================
"""
This module defines the API endpoint for the health check service.

It provides a simple '/health' route that can be used to monitor the
application's status and verify its current version.
"""

# =======================================================================
# ⚙️ 1. IMPORTS
# =======================================================================
import logging
from pathlib import Path

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from ..services import health as health_service

from src.utils.constants import FINAL_OPENAPI_PATH

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =======================================================================
# 🚀 2. API ROUTER CONFIGURATION
# =======================================================================
router = APIRouter(
    tags=["health"],
)


# =======================================================================
# 🔗 3. API ENDPOINT
# =======================================================================
@router.get("/health")
async def get_health_status_endpoint(request: Request):
    """
    API endpoint to check the health of the service.

    This endpoint calls the health controller to get the application's
    status and returns it in a JSON response.
    """
    # Retrieve the status from the controller.
    version, error = health_service.get_health_status()

    # The controller currently returns version information on success.
    if version is not None:
        content_response = {"status": "ok", "version": version}
        logger.info("Health check successful.")
        return JSONResponse(status_code=200, content=content_response)
    else:
        # If the controller returns an error, log it and raise an exception.
        logger.warning(f"Health check failed: {error}")
        raise HTTPException(status_code=500, detail=f"Health check failed with error: {error}")


@router.get(
    "/openapi",
    summary="Download OpenAPI YAML",
    response_description="Your full OpenAPI spec in YAML",
)
async def download_openapi_yaml():
    """
    Serves the pre-built OpenAPI YAML file for API Gateway import
    (and for developers to download).
    """
    openapi_path = Path(FINAL_OPENAPI_PATH)

    if not openapi_path.exists():
        logger.error(f"OpenAPI file not found at {FINAL_OPENAPI_PATH}")
        raise HTTPException(status_code=404, detail="OpenAPI spec not found")

    try:
        return FileResponse(
            path=str(openapi_path),
            media_type="application/x-yaml",
            filename=openapi_path.name,
        )
    except Exception as e:
        logger.error(f"Failed to serve OpenAPI YAML: {e}")
        raise HTTPException(status_code=500, detail="Could not load OpenAPI YAML file")
