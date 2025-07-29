"""
Repository layer initialization module.

This module initializes the repository layer, which provides data access operations
for the application's models. It exports repository objects that can be imported
and used throughout the application.
"""

from app.repositories.item_repository import item

__all__ = ["item"]
