"""Domain entities for the TODO application.

This module contains pure domain objects that represent business entities
without any infrastructure dependencies.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TaskEntity:
    """Task entity representing a single task in the domain.
    
    This is a pure domain object without any SQLAlchemy or infrastructure
    dependencies. It represents the business concept of a task.
    
    Attributes:
        id: Unique identifier for the task.
        title: Task title (required, max 200 characters).
        description: Optional detailed description of the task.
        created_at: Timestamp when the task was created.
        completed_at: Timestamp when the task was completed (None if not completed).
    """
    id: int | None = None
    title: str = ""
    description: str | None = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None

    @property
    def is_completed(self) -> bool:
        """Check if the task is completed.
        
        Returns:
            bool: True if the task has a completed_at timestamp, False otherwise.
        """
        return self.completed_at is not None

    def mark_completed(self) -> None:
        """Mark the task as completed by setting the completed_at timestamp."""
        if not self.is_completed:
            self.completed_at = datetime.now()

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete by clearing the completed_at timestamp."""
        self.completed_at = None

    def get_completion_date_str(self) -> str:
        """Get the completion date as a formatted string.
        
        Returns:
            str: Formatted date string (DD/MM) or empty string if not completed.
        """
        if self.completed_at:
            return self.completed_at.strftime("%d/%m")
        return ""

    def get_created_date_str(self) -> str:
        """Get the creation date as a formatted string.
        
        Returns:
            str: Formatted date string (DD/MM/YYYY).
        """
        return self.created_at.strftime("%d/%m/%Y")

    def get_created_time_str(self) -> str:
        """Get the creation time as a formatted string.
        
        Returns:
            str: Formatted time string (HH:MM).
        """
        return self.created_at.strftime("%H:%M")

    def validate(self) -> tuple[bool, str | None]:
        """Validate the task entity.
        
        Returns:
            tuple[bool, Optional[str]]: A tuple of (is_valid, error_message).
        """
        if not self.title or not self.title.strip():
            return False, "Task title cannot be empty"

        if len(self.title) > 200:
            return False, "Task title must not exceed 200 characters"

        return True, None
