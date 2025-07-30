# src/utils/logging.py
import logging
import json
from datetime import datetime, UTC


class JSONFormatter(logging.Formatter):
    """
    Custom formatter to output log records as a JSON string.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats a log record into a JSON string.

        Args:
            record: The original log record.

        Returns:
            A JSON string representing the log record.
        """
        log_object = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.name,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }
        return json.dumps(log_object)


def configure_logging():
    """
    Configures the root logger for the application.

    This function removes any existing handlers, adds a new stream handler
    with the custom JSON formatter, and sets the logging level to INFO.
    This ensures all log output is in a structured JSON format.
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Remove any existing handlers to prevent duplicate logs
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Create a new handler and formatter
    handler = logging.StreamHandler()
    formatter = JSONFormatter()
    handler.setFormatter(formatter)

    # Add the new handler to the root logger
    root_logger.addHandler(handler)
