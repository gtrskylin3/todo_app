"""Application configuration module.

This module provides configuration settings for the application including
database paths, logging settings, and application constants.
"""

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DatabaseConfig:
    """Database configuration settings.
    
    Attributes:
        db_path: Path to the SQLite database file.
        echo: Whether to echo SQL statements for debugging.
    """
    db_path: str
    echo: bool = False


@dataclass(frozen=True)
class LoggingConfig:
    """Logging configuration settings.
    
    Attributes:
        log_file: Path to the log file.
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_format: Format string for log messages.
    """
    log_file: str
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass(frozen=True)
class AppConfig:
    """Main application configuration.
    
    Attributes:
        app_name: Name of the application.
        version: Application version.
        database: Database configuration.
        logging: Logging configuration.
    """
    app_name: str = "TODO Application"
    version: str = "1.0.0"
    database: DatabaseConfig = None  # type: ignore
    logging: LoggingConfig = None  # type: ignore


def get_app_config() -> AppConfig:
    """Get application configuration based on environment.
    
    Returns:
        AppConfig: Application configuration object.
    """
    # Get the base directory (where main.py is located)
    base_dir = Path(__file__).parent.parent.parent

    # Database configuration
    db_path = os.getenv(
        "TODO_DB_PATH",
        str(base_dir / "data" / "todo.db")
    )

    # Ensure data directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    # Logging configuration
    log_file = os.getenv(
        "TODO_LOG_PATH",
        str(base_dir / "logs" / "app.log")
    )

    # Ensure logs directory exists
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    return AppConfig(
        app_name="TODO Application",
        version="1.0.0",
        database=DatabaseConfig(
            db_path=db_path,
            echo=os.getenv("TODO_DB_ECHO", "false").lower() == "true"
        ),
        logging=LoggingConfig(
            log_file=log_file,
            log_level=os.getenv("TODO_LOG_LEVEL", "INFO")
        )
    )
