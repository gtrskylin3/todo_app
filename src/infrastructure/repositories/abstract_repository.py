"""Abstract repository for task data access.

This module defines the interface for task repositories, ensuring
the domain layer is decoupled from the infrastructure implementation.
"""

from abc import ABC, abstractmethod
from datetime import datetime

from src.domain.task_entity import TaskEntity


class AbstractTaskRepository(ABC):
    """Abstract base class for task repositories.
    
    This class defines the contract that all task repository implementations
    must follow. It uses the Repository Pattern to abstract data access.
    """

    @abstractmethod
    def add(self, task: TaskEntity) -> TaskEntity:
        """Add a new task to the repository.
        
        Args:
            task: The task entity to add.
            
        Returns:
            TaskEntity: The added task with its ID populated.
        """
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> TaskEntity | None:
        """Get a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve.
            
        Returns:
            Optional[TaskEntity]: The task entity if found, None otherwise.
        """
        pass

    @abstractmethod
    def get_all_active(self) -> list[TaskEntity]:
        """Get all non-completed tasks.
        
        Returns:
            list[TaskEntity]: List of active (non-completed) tasks.
        """
        pass

    @abstractmethod
    def get_completed_by_date(self, date: datetime) -> list[TaskEntity]:
        """Get all tasks completed on a specific date.
        
        Args:
            date: The date to filter completed tasks by.
            
        Returns:
            list[TaskEntity]: List of tasks completed on the specified date.
        """
        pass

    @abstractmethod
    def get_all_completed_dates(self) -> list[datetime]:
        """Get all unique dates when tasks were completed.
        
        Returns:
            list[datetime]: List of unique completion dates in descending order.
        """
        pass

    @abstractmethod
    def update(self, task: TaskEntity) -> TaskEntity:
        """Update an existing task.
        
        Args:
            task: The task entity with updated values.
            
        Returns:
            TaskEntity: The updated task entity.
            
        Raises:
            ValueError: If the task does not exist.
        """
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID.
        
        Args:
            task_id: The ID of the task to delete.
            
        Returns:
            bool: True if the task was deleted, False if it didn't exist.
        """
        pass

    @abstractmethod
    def toggle_completion(self, task_id: int) -> TaskEntity | None:
        """Toggle the completion status of a task.
        
        Args:
            task_id: The ID of the task to toggle.
            
        Returns:
            Optional[TaskEntity]: The updated task entity if found, None otherwise.
        """
        pass

    @abstractmethod
    def reopen(self, task_id: int) -> TaskEntity | None:
        """Reopen a completed task (mark as incomplete).
        
        Args:
            task_id: The ID of the task to reopen.
            
        Returns:
            Optional[TaskEntity]: The updated task entity if found, None otherwise.
        """
        pass
