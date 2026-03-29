"""Main entry point for the TODO application.

This module initializes the application, sets up dependency injection,
and starts the PyQt6 event loop.
"""

import sys
import logging

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QFontDatabase

from src.config.settings import get_app_config, AppConfig
from src.config.logging_config import setup_logging
from src.infrastructure.db.database import create_database_engine, create_session_factory
from src.infrastructure.repositories.sqlalchemy_repository import SQLAlchemyTaskRepository
from src.application.task_service import TaskService
from src.presentation.views.main_window import MainWindow


def create_application(config: AppConfig) -> QApplication:
    """Create and configure the Qt application.
    
    Args:
        config: Application configuration.
        
    Returns:
        QApplication: Configured Qt application instance.
    """
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = QApplication(sys.argv)
    app.setApplicationName(config.app_name)
    app.setApplicationVersion(config.version)
    
    # Set default font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    return app


def create_dependencies(config: AppConfig) -> tuple[TaskService, SQLAlchemyTaskRepository]:
    """Create and wire up application dependencies.
    
    This function implements dependency injection by creating the database
    engine, repository, and service layer.
    
    Args:
        config: Application configuration.
        
    Returns:
        tuple[TaskService, SQLAlchemyTaskRepository]: Service and repository instances.
    """
    # Create database engine and session factory
    engine = create_database_engine(config.database)
    session_factory = create_session_factory(engine)
    
    # Create repository
    repository = SQLAlchemyTaskRepository(session_factory)
    
    # Create service
    task_service = TaskService(repository)
    
    return task_service, repository


def main() -> int:
    """Main entry point for the application.
    
    Returns:
        int: Application exit code.
    """
    # Load configuration
    config = get_app_config()
    
    # Setup logging
    logger = setup_logging(config.logging)
    logger.info(f"Starting {config.app_name} v{config.version}")
    logger.info(f"Database path: {config.database.db_path}")
    logger.info(f"Log file: {config.logging.log_file}")
    
    try:
        # Create Qt application
        app = create_application(config)
        
        # Create dependencies with dependency injection
        task_service, repository = create_dependencies(config)
        
        # Create and show main window
        window = MainWindow(task_service, config)
        window.show()
        
        logger.info("Application started successfully")
        
        # Run event loop
        return app.exec()
        
    except Exception as e:
        logger.exception(f"Application error: {e}")
        return 1
    
    finally:
        logger.info("Application shutting down")


if __name__ == "__main__":
    sys.exit(main())
