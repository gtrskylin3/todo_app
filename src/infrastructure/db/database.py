"""Database engine and session management.

This module provides database engine creation and session factory
for SQLAlchemy operations.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.config.settings import DatabaseConfig

# Base class for all models
Base = declarative_base()


def create_database_engine(config: DatabaseConfig):
    """Create a SQLAlchemy database engine.
    
    Args:
        config: Database configuration settings.
        
    Returns:
        Engine: SQLAlchemy engine instance.
    """
    # Use SQLite with check_same_thread=False for compatibility with PyQt threads
    engine = create_engine(
        f"sqlite:///{config.db_path}",
        echo=config.echo,
        connect_args={"check_same_thread": False},
        future=True
    )

    # Create all tables
    Base.metadata.create_all(engine)

    return engine


def create_session_factory(engine) -> sessionmaker:
    """Create a session factory bound to the engine.
    
    Args:
        engine: SQLAlchemy engine instance.
        
    Returns:
        sessionmaker: Configured session factory.
    """
    return sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=Session
    )
