"""Application services for task management.

This module contains the TaskService class which orchestrates business logic
between the domain layer and infrastructure layer. It is UI-agnostic.
"""

import logging
from datetime import datetime
from typing import NamedTuple

from src.domain.task_entity import TaskEntity
from src.infrastructure.repositories.abstract_repository import AbstractTaskRepository

logger = logging.getLogger(__name__)


class TaskValidationError(Exception):
    """Exception raised when task validation fails."""
    pass


class TaskServiceResult(NamedTuple):
    """Result of a task service operation.
    
    Attributes:
        success: Whether the operation was successful.
        task: The task entity if the operation was successful.
        error: Error message if the operation failed.
    """
    success: bool
    task: TaskEntity | None = None
    error: str | None = None


class TaskService:
    """Service class for task-related business logic.
    
    This class provides use cases for task management operations.
    It is designed to be UI-agnostic and can be used by any presentation layer.
    
    Args:
        repository: Task repository implementation for data access.
    """

    def __init__(self, repository: AbstractTaskRepository):
        """Initialize the service with a task repository.
        
        Args:
            repository: Task repository implementation.
        """
        self._repository = repository

    def create_task(self, title: str, description: str | None = None) -> TaskServiceResult:
        """Create a new task.
        
        Args:
            title: Task title (required).
            description: Optional task description.
            
        Returns:
            TaskServiceResult: Result of the operation.
        """
        # Create entity and validate
        task = TaskEntity(
            title=title.strip() if title else "",
            description=description.strip() if description else None
        )

        is_valid, error_message = task.validate()
        if not is_valid:
            logger.warning(f"Task validation failed: {error_message}")
            return TaskServiceResult(success=False, error=error_message)

        try:
            saved_task = self._repository.add(task)
            logger.info(f"Created task: {saved_task.title}")
            return TaskServiceResult(success=True, task=saved_task)
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            return TaskServiceResult(success=False, error=str(e))

    def get_task(self, task_id: int) -> TaskEntity | None:
        """Get a task by ID.
        
        Args:
            task_id: Task ID to retrieve.
            
        Returns:
            Optional[TaskEntity]: Task entity if found, None otherwise.
        """
        return self._repository.get_by_id(task_id)

    def get_all_active_tasks(self) -> list[TaskEntity]:
        """Get all active (non-completed) tasks.

        Returns:
            list[TaskEntity]: List of active tasks.
        """
        return self._repository.get_all_active()

    def get_todays_tasks(self) -> list[TaskEntity]:
        """Get tasks created today.

        Returns:
            list[TaskEntity]: List of tasks created today.
        """
        today = datetime.now().date()
        all_active = self._repository.get_all_active()
        return [task for task in all_active 
                if task.created_at.date() == today]

    def get_completed_tasks_by_date(self, date_value: datetime) -> list[TaskEntity]:
        """Get tasks completed on a specific date.
        
        Args:
            date_value: Date to filter by.
            
        Returns:
            list[TaskEntity]: List of tasks completed on the date.
        """
        return self._repository.get_completed_by_date(date_value)

    def get_all_completed_dates(self) -> list[datetime]:
        """Get all unique dates with completed tasks.
        
        Returns:
            list[datetime]: List of completion dates.
        """
        return self._repository.get_all_completed_dates()

    def update_task(
        self,
        task_id: int,
        title: str,
        description: str | None = None
    ) -> TaskServiceResult:
        """Update an existing task.
        
        Args:
            task_id: ID of the task to update.
            title: New task title.
            description: New task description.
            
        Returns:
            TaskServiceResult: Result of the operation.
        """
        existing_task = self._repository.get_by_id(task_id)
        if not existing_task:
            logger.warning(f"Task {task_id} not found for update")
            return TaskServiceResult(success=False, error="Task not found")

        # Create updated entity and validate
        task = TaskEntity(
            id=task_id,
            title=title.strip() if title else "",
            description=description.strip() if description else None,
            created_at=existing_task.created_at,
            completed_at=existing_task.completed_at
        )

        is_valid, error_message = task.validate()
        if not is_valid:
            logger.warning(f"Task validation failed: {error_message}")
            return TaskServiceResult(success=False, error=error_message)

        try:
            updated_task = self._repository.update(task)
            logger.info(f"Updated task: {updated_task.title}")
            return TaskServiceResult(success=True, task=updated_task)
        except Exception as e:
            logger.error(f"Failed to update task: {e}")
            return TaskServiceResult(success=False, error=str(e))

    def delete_task(self, task_id: int) -> TaskServiceResult:
        """Delete a task.
        
        Args:
            task_id: ID of the task to delete.
            
        Returns:
            TaskServiceResult: Result of the operation.
        """
        try:
            deleted = self._repository.delete(task_id)
            if deleted:
                logger.info(f"Deleted task {task_id}")
                return TaskServiceResult(success=True)
            else:
                logger.warning(f"Task {task_id} not found for deletion")
                return TaskServiceResult(success=False, error="Task not found")
        except Exception as e:
            logger.error(f"Failed to delete task: {e}")
            return TaskServiceResult(success=False, error=str(e))

    def toggle_task_completion(self, task_id: int) -> TaskServiceResult:
        """Toggle the completion status of a task.
        
        Args:
            task_id: ID of the task to toggle.
            
        Returns:
            TaskServiceResult: Result of the operation.
        """
        try:
            task = self._repository.toggle_completion(task_id)
            if task:
                status = "completed" if task.is_completed else "reopened"
                logger.info(f"Task {task_id} {status}")
                return TaskServiceResult(success=True, task=task)
            else:
                return TaskServiceResult(success=False, error="Task not found")
        except Exception as e:
            logger.error(f"Failed to toggle task completion: {e}")
            return TaskServiceResult(success=False, error=str(e))

    def reopen_task(self, task_id: int) -> TaskServiceResult:
        """Reopen a completed task.
        
        Args:
            task_id: ID of the task to reopen.
            
        Returns:
            TaskServiceResult: Result of the operation.
        """
        try:
            task = self._repository.reopen(task_id)
            if task:
                logger.info(f"Reopened task {task_id}")
                return TaskServiceResult(success=True, task=task)
            else:
                return TaskServiceResult(success=False, error="Task not found")
        except Exception as e:
            logger.error(f"Failed to reopen task: {e}")
            return TaskServiceResult(success=False, error=str(e))

    def format_date_for_display(self, date_value: datetime) -> str:
        """Format a date for display in the UI.
        
        Args:
            date_value: Date to format.
            
        Returns:
            str: Formatted date string (e.g., "25 March 2026").
        """
        return date_value.strftime("%d %B %Y")

    def format_date_short(self, date_value: datetime) -> str:
        """Format a date in short format.
        
        Args:
            date_value: Date to format.
            
        Returns:
            str: Formatted date string (DD/MM).
        """
        return date_value.strftime("%d/%m")
