"""Logging configuration module.

This module sets up logging for the application with both file and console handlers.
"""

import logging
import sys

from src.config.settings import LoggingConfig


def setup_logging(config: LoggingConfig) -> logging.Logger:
    """Configure and return the application logger.
    
    Args:
        config: Logging configuration settings.
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create logger
    logger = logging.getLogger("todo_app")
    logger.setLevel(getattr(logging, config.log_level))

    # Clear existing handlers
    logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(config.log_format)

    # File handler
    file_handler = logging.FileHandler(config.log_file, encoding="utf-8")
    file_handler.setLevel(getattr(logging, config.log_level))
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, config.log_level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
