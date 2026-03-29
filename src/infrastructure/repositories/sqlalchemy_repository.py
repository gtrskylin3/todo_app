"""SQLAlchemy implementation of the task repository.

This module provides the concrete implementation of the task repository
using SQLAlchemy for database operations.
"""

import logging
from datetime import datetime

from sqlalchemy.orm import Session

from src.domain.task_entity import TaskEntity
from src.infrastructure.db.models import TaskModel
from src.infrastructure.repositories.abstract_repository import AbstractTaskRepository

logger = logging.getLogger(__name__)


class SQLAlchemyTaskRepository(AbstractTaskRepository):
    """SQLAlchemy implementation of the task repository.
    
    This class provides concrete database operations for task management
    using SQLAlchemy ORM. It implements the AbstractTaskRepository interface.
    
    Args:
        session_factory: SQLAlchemy session factory for creating database sessions.
    """

    def __init__(self, session_factory):
        """Initialize the repository with a session factory.
        
        Args:
            session_factory: SQLAlchemy session factory.
        """
        self._session_factory = session_factory

    def _get_session(self) -> Session:
        """Get a new database session.
        
        Returns:
            Session: SQLAlchemy session instance.
        """
        return self._session_factory()

    def add(self, task: TaskEntity) -> TaskEntity:
        """Add a new task to the database.
        
        Args:
            task: The task entity to add.
            
        Returns:
            TaskEntity: The added task with its ID populated.
        """
        session = self._get_session()
        try:
            model = TaskModel.from_entity(task)
            session.add(model)
            session.commit()
            session.refresh(model)

            logger.debug(f"Added task with ID {model.id}: {task.title}")
            return model.to_entity()
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to add task: {e}")
            raise
        finally:
            session.close()

    def get_by_id(self, task_id: int) -> TaskEntity | None:
        """Get a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve.
            
        Returns:
            Optional[TaskEntity]: The task entity if found, None otherwise.
        """
        session = self._get_session()
        try:
            model = session.query(TaskModel).filter(TaskModel.id == task_id).first()
            if model:
                return model.to_entity()
            logger.debug(f"Task with ID {task_id} not found")
            return None
        except Exception as e:
            logger.error(f"Failed to get task by ID {task_id}: {e}")
            raise
        finally:
            session.close()

    def get_all_active(self) -> list[TaskEntity]:
        """Get all non-completed tasks ordered by creation date.
        
        Returns:
            list[TaskEntity]: List of active (non-completed) tasks.
        """
        session = self._get_session()
        try:
            models = (
                session.query(TaskModel)
                .filter(TaskModel.completed_at.is_(None))
                .order_by(TaskModel.created_at.desc())
                .all()
            )
            return [model.to_entity() for model in models]
        except Exception as e:
            logger.error(f"Failed to get active tasks: {e}")
            raise
        finally:
            session.close()

    def get_completed_by_date(self, date_value: datetime) -> list[TaskEntity]:
        """Get all tasks completed on a specific date.
        
        Args:
            date_value: The date to filter completed tasks by.
            
        Returns:
            list[TaskEntity]: List of tasks completed on the specified date.
        """
        session = self._get_session()
        try:
            # Extract just the date part for comparison
            target_date = date_value.date() if isinstance(date_value, datetime) else date_value

            models = (
                session.query(TaskModel)
                .filter(
                    TaskModel.completed_at.isnot(None),
                    TaskModel.completed_at >= datetime.combine(target_date, datetime.min.time()),
                    TaskModel.completed_at < datetime.combine(target_date, datetime.max.time())
                )
                .order_by(TaskModel.completed_at.desc())
                .all()
            )
            return [model.to_entity() for model in models]
        except Exception as e:
            logger.error(f"Failed to get completed tasks for date {date_value}: {e}")
            raise
        finally:
            session.close()

    def get_all_completed_dates(self) -> list[datetime]:
        """Get all unique dates when tasks were completed.
        
        Returns:
            list[datetime]: List of unique completion dates in descending order.
        """
        session = self._get_session()
        try:
            # Query distinct completion dates
            results = (
                session.query(TaskModel.completed_at)
                .filter(TaskModel.completed_at.isnot(None))
                .distinct()
                .order_by(TaskModel.completed_at.desc())
                .all()
            )

            # Extract unique dates
            dates = []
            seen_dates = set()
            for (completed_at,) in results:
                if completed_at:
                    date_only = completed_at.date()
                    if date_only not in seen_dates:
                        seen_dates.add(date_only)
                        dates.append(completed_at)

            return dates
        except Exception as e:
            logger.error(f"Failed to get completed dates: {e}")
            raise
        finally:
            session.close()

    def update(self, task: TaskEntity) -> TaskEntity:
        """Update an existing task in the database.
        
        Args:
            task: The task entity with updated values.
            
        Returns:
            TaskEntity: The updated task entity.
            
        Raises:
            ValueError: If the task does not exist.
        """
        session = self._get_session()
        try:
            model = session.query(TaskModel).filter(TaskModel.id == task.id).first()
            if not model:
                raise ValueError(f"Task with ID {task.id} not found")

            model.title = task.title
            model.description = task.description
            model.created_at = task.created_at
            model.completed_at = task.completed_at

            session.commit()
            session.refresh(model)

            logger.debug(f"Updated task with ID {task.id}: {task.title}")
            return model.to_entity()
        except ValueError:
            raise
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to update task {task.id}: {e}")
            raise
        finally:
            session.close()

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID.
        
        Args:
            task_id: The ID of the task to delete.
            
        Returns:
            bool: True if the task was deleted, False if it didn't exist.
        """
        session = self._get_session()
        try:
            model = session.query(TaskModel).filter(TaskModel.id == task_id).first()
            if not model:
                logger.debug(f"Task with ID {task_id} not found, nothing to delete")
                return False

            session.delete(model)
            session.commit()

            logger.debug(f"Deleted task with ID {task_id}")
            return True
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to delete task {task_id}: {e}")
            raise
        finally:
            session.close()

    def toggle_completion(self, task_id: int) -> TaskEntity | None:
        """Toggle the completion status of a task.
        
        If the task is incomplete, it marks it as completed with the current timestamp.
        If the task is completed, it marks it as incomplete.
        
        Args:
            task_id: The ID of the task to toggle.
            
        Returns:
            Optional[TaskEntity]: The updated task entity if found, None otherwise.
        """
        session = self._get_session()
        try:
            model = session.query(TaskModel).filter(TaskModel.id == task_id).first()
            if not model:
                logger.debug(f"Task with ID {task_id} not found")
                return None

            if model.completed_at is None:
                model.completed_at = datetime.now()
                logger.debug(f"Completed task with ID {task_id}")
            else:
                model.completed_at = None
                logger.debug(f"Reopened task with ID {task_id}")

            session.commit()
            session.refresh(model)
            return model.to_entity()
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to toggle task {task_id}: {e}")
            raise
        finally:
            session.close()

    def reopen(self, task_id: int) -> TaskEntity | None:
        """Reopen a completed task (mark as incomplete).
        
        Args:
            task_id: The ID of the task to reopen.
            
        Returns:
            Optional[TaskEntity]: The updated task entity if found, None otherwise.
        """
        session = self._get_session()
        try:
            model = session.query(TaskModel).filter(TaskModel.id == task_id).first()
            if not model:
                logger.debug(f"Task with ID {task_id} not found")
                return None

            model.completed_at = None
            session.commit()
            session.refresh(model)

            logger.debug(f"Reopened task with ID {task_id}")
            return model.to_entity()
        except Exception as e:
            session.rollback()
            logger.error(f"Failed to reopen task {task_id}: {e}")
            raise
        finally:
            session.close()
