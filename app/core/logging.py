"""
Logging configuration module for the application.

This module provides structured logging setup using the structlog library,
which enables rich, contextual logs that can be easily parsed and analyzed.
The configuration adapts based on the environment (development vs. production).
"""

import logging  # Standard library logging module
import sys  # For stdout access
from typing import Optional  # Type hints

# Structured logging library
import structlog
from structlog.types import Processor  # Type for log processors

# Application settings
from app.core.config import settings


def configure_logging() -> None:
    """
    Configure structured logging for the application.

    This function sets up the logging system with appropriate processors
    and formatters based on the current environment. In development,
    it uses a human-readable console output, while in production it
    outputs JSON for easier parsing by log aggregation tools.
    """
    # Define the chain of log processors that will handle each log entry
    processors: list[Processor] = [
        # Add context variables from the current execution context
        structlog.contextvars.merge_contextvars,

        # Filter logs based on their level (DEBUG, INFO, etc.)
        structlog.stdlib.filter_by_level,

        # Add the logger name to each log entry
        structlog.stdlib.add_logger_name,

        # Add the log level to each log entry
        structlog.stdlib.add_log_level,

        # Format positional arguments in log messages
        structlog.stdlib.PositionalArgumentsFormatter(),

        # Add ISO-format timestamp to each log entry
        structlog.processors.TimeStamper(fmt="iso"),

        # Add stack information for better debugging
        structlog.processors.StackInfoRenderer(),

        # Format exception information if present
        structlog.processors.format_exc_info,
    ]

    # In development, use a human-readable console formatter
    if settings.ENVIRONMENT == "development":
        # Add console renderer for human-readable logs
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        # In production, use JSON formatter for easier parsing by log aggregators
        processors.append(structlog.processors.JSONRenderer())

    # Configure structlog with our processors and settings
    structlog.configure(
        processors=processors,  # Chain of processors to apply to each log
        logger_factory=structlog.stdlib.LoggerFactory(),  # Use standard library's logger
        wrapper_class=structlog.stdlib.BoundLogger,  # Logger class to use
        cache_logger_on_first_use=True,  # Cache loggers for performance
    )

    # Set the log level based on the environment
    # In development, we want more detailed logs (DEBUG level)
    log_level = logging.DEBUG if settings.ENVIRONMENT == "development" else logging.INFO

    # Configure the standard library logging
    logging.basicConfig(
        format="%(message)s",  # Simple format as structlog handles the formatting
        level=log_level,  # Set log level from environment
        stream=sys.stdout,  # Output logs to standard output
    )


def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """
    Get a structured logger with the given name.

    Args:
        name: The name for the logger, typically the module name (__name__)

    Returns:
        A configured structlog BoundLogger instance that can be used for logging

    Example:
        logger = get_logger(__name__)
        logger.info("This is an info message", extra_field="some value")
    """
    return structlog.get_logger(name)
