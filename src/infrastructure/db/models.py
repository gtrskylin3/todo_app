"""SQLAlchemy models for the TODO application.

This module defines the database schema using SQLAlchemy ORM.
"""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.db.database import Base


class TaskModel(Base):
    """SQLAlchemy model for the tasks table.
    
    This model maps to the 'tasks' table in the database and provides
    the infrastructure layer for task persistence.
    
    Attributes:
        id: Primary key, auto-incrementing integer.
        title: Task title, required, max 200 characters.
        description: Optional task description.
        created_at: Timestamp of task creation, auto-generated.
        completed_at: Timestamp of task completion, nullable.
        is_completed: Computed boolean based on completed_at.
    """
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False,
        index=True
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        index=True
    )

    @property
    def is_completed(self) -> bool:
        """Check if the task is completed.
        
        Returns:
            bool: True if completed_at is set, False otherwise.
        """
        return self.completed_at is not None

    def to_entity(self) -> "TaskEntity":
        """Convert the model to a domain entity.
        
        Returns:
            TaskEntity: Domain entity representation of this model.
        """
        # Import here to avoid circular dependency
        from src.domain.task_entity import TaskEntity

        return TaskEntity(
            id=self.id,
            title=self.title,
            description=self.description,
            created_at=self.created_at,
            completed_at=self.completed_at
        )

    @classmethod
    def from_entity(cls, entity: "TaskEntity") -> "TaskModel":
        """Create a model from a domain entity.
        
        Args:
            entity: Domain entity to convert.
            
        Returns:
            TaskModel: Model instance populated from the entity.
        """
        return cls(
            id=entity.id,
            title=entity.title,
            description=entity.description,
            created_at=entity.created_at,
            completed_at=entity.completed_at
        )
