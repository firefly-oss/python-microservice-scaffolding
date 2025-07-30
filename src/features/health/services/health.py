# src/api/features/health/services/health.py
# =======================================================================
# 📝 FILE OVERVIEW
# =======================================================================
"""
This module contains the service logic for the health check service.

It provides the core logic for the health check endpoint, returning the
current API version to indicate that the service is operational.
"""

# =======================================================================
# ⚙️ 1. IMPORTS & CONFIGURATION
# =======================================================================
import os
from typing import Tuple, Optional

# The version of the API, retrieved from the 'API_VERSION' environment
# variable. Defaults to '0.0.0' if not set.
API_VERSION: str = os.getenv("API_VERSION", "0.0.0")


# =======================================================================
# 🚀 2. SERVICE FUNCTION
# =======================================================================
def get_health_status() -> Tuple[str, Optional[None]]:
    """
    Provides the health status of the API.

    This service function currently returns the API version and a None
    value, adhering to a simple success-tuple format. In the future, it
    could be expanded to check dependencies like databases or other services.

    Returns:
        A tuple containing the API version and None.
    """
    return API_VERSION, None
