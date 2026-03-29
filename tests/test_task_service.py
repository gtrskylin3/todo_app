"""Unit tests for the TaskService layer.

This module contains pytest tests for the application service layer,
testing business logic and validation.
"""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.application.task_service import TaskService
from src.domain.task_entity import TaskEntity


@pytest.fixture
def mock_repository():
    """Create a mock repository for testing."""
    repo = MagicMock()
    repo.add = MagicMock()
    repo.get_by_id = MagicMock()
    repo.get_all_active = MagicMock()
    repo.get_completed_by_date = MagicMock()
    repo.get_all_completed_dates = MagicMock()
    repo.update = MagicMock()
    repo.delete = MagicMock()
    repo.toggle_completion = MagicMock()
    repo.reopen = MagicMock()
    return repo


@pytest.fixture
def task_service(mock_repository):
    """Create a TaskService with mock repository."""
    return TaskService(mock_repository)


class TestTaskServiceCreateTask:
    """Tests for TaskService.create_task method."""

    def test_create_task_success(self, task_service, mock_repository):
        """Test successful task creation."""
        # Arrange
        mock_repository.add.return_value = TaskEntity(
            id=1,
            title="Test Task",
            description="Test Description"
        )

        # Act
        result = task_service.create_task("Test Task", "Test Description")

        # Assert
        assert result.success is True
        assert result.task is not None
        assert result.task.title == "Test Task"
        assert result.error is None
        mock_repository.add.assert_called_once()

    def test_create_task_empty_title(self, task_service, mock_repository):
        """Test task creation with empty title."""
        # Act
        result = task_service.create_task("")

        # Assert
        assert result.success is False
        assert result.task is None
        assert result.error == "Task title cannot be empty"
        mock_repository.add.assert_not_called()

    def test_create_task_whitespace_title(self, task_service, mock_repository):
        """Test task creation with whitespace-only title."""
        # Act
        result = task_service.create_task("   ")

        # Assert
        assert result.success is False
        assert result.task is None
        assert result.error == "Task title cannot be empty"
        mock_repository.add.assert_not_called()

    def test_create_task_title_too_long(self, task_service, mock_repository):
        """Test task creation with title exceeding 200 characters."""
        # Arrange
        long_title = "A" * 201

        # Act
        result = task_service.create_task(long_title)

        # Assert
        assert result.success is False
        assert result.error == "Task title must not exceed 200 characters"
        mock_repository.add.assert_not_called()

    def test_create_task_strips_whitespace(self, task_service, mock_repository):
        """Test that task creation strips whitespace from title and description."""
        # Arrange
        mock_repository.add.return_value = TaskEntity(
            id=1,
            title="Test Task",
            description="Test Description"
        )

        # Act
        result = task_service.create_task("  Test Task  ", "  Test Description  ")

        # Assert
        assert result.success is True
        mock_repository.add.assert_called_once()
        call_args = mock_repository.add.call_args[0][0]
        assert call_args.title == "Test Task"
        assert call_args.description == "Test Description"

    def test_create_task_without_description(self, task_service, mock_repository):
        """Test task creation without description."""
        # Arrange
        mock_repository.add.return_value = TaskEntity(
            id=1,
            title="Test Task"
        )

        # Act
        result = task_service.create_task("Test Task")

        # Assert
        assert result.success is True
        assert result.task is not None


class TestTaskServiceUpdateTask:
    """Tests for TaskService.update_task method."""

    def test_update_task_success(self, task_service, mock_repository):
        """Test successful task update."""
        # Arrange
        existing_task = TaskEntity(
            id=1,
            title="Old Title",
            created_at=datetime.now()
        )
        updated_task = TaskEntity(
            id=1,
            title="New Title",
            description="New Description",
            created_at=existing_task.created_at
        )
        mock_repository.get_by_id.return_value = existing_task
        mock_repository.update.return_value = updated_task

        # Act
        result = task_service.update_task(1, "New Title", "New Description")

        # Assert
        assert result.success is True
        assert result.task is not None
        assert result.task.title == "New Title"

    def test_update_task_not_found(self, task_service, mock_repository):
        """Test update when task doesn't exist."""
        # Arrange
        mock_repository.get_by_id.return_value = None

        # Act
        result = task_service.update_task(999, "New Title")

        # Assert
        assert result.success is False
        assert result.error == "Task not found"

    def test_update_task_empty_title(self, task_service, mock_repository):
        """Test update with empty title."""
        # Arrange
        mock_repository.get_by_id.return_value = TaskEntity(
            id=1,
            title="Old Title"
        )

        # Act
        result = task_service.update_task(1, "")

        # Assert
        assert result.success is False
        assert result.error == "Task title cannot be empty"


class TestTaskServiceDeleteTask:
    """Tests for TaskService.delete_task method."""

    def test_delete_task_success(self, task_service, mock_repository):
        """Test successful task deletion."""
        # Arrange
        mock_repository.delete.return_value = True

        # Act
        result = task_service.delete_task(1)

        # Assert
        assert result.success is True
        mock_repository.delete.assert_called_once_with(1)

    def test_delete_task_not_found(self, task_service, mock_repository):
        """Test deletion of non-existent task."""
        # Arrange
        mock_repository.delete.return_value = False

        # Act
        result = task_service.delete_task(999)

        # Assert
        assert result.success is False
        assert result.error == "Task not found"


class TestTaskServiceToggleCompletion:
    """Tests for TaskService.toggle_task_completion method."""

    def test_toggle_task_success(self, task_service, mock_repository):
        """Test successful task completion toggle."""
        # Arrange
        toggled_task = TaskEntity(
            id=1,
            title="Test Task",
            completed_at=datetime.now()
        )
        mock_repository.toggle_completion.return_value = toggled_task

        # Act
        result = task_service.toggle_task_completion(1)

        # Assert
        assert result.success is True
        assert result.task is not None
        assert result.task.is_completed is True

    def test_toggle_task_not_found(self, task_service, mock_repository):
        """Test toggle when task doesn't exist."""
        # Arrange
        mock_repository.toggle_completion.return_value = None

        # Act
        result = task_service.toggle_task_completion(999)

        # Assert
        assert result.success is False
        assert result.error == "Task not found"


class TestTaskServiceReopenTask:
    """Tests for TaskService.reopen_task method."""

    def test_reopen_task_success(self, task_service, mock_repository):
        """Test successful task reopen."""
        # Arrange
        reopened_task = TaskEntity(
            id=1,
            title="Test Task",
            completed_at=None
        )
        mock_repository.reopen.return_value = reopened_task

        # Act
        result = task_service.reopen_task(1)

        # Assert
        assert result.success is True
        assert result.task is not None
        assert result.task.is_completed is False

    def test_reopen_task_not_found(self, task_service, mock_repository):
        """Test reopen when task doesn't exist."""
        # Arrange
        mock_repository.reopen.return_value = None

        # Act
        result = task_service.reopen_task(999)

        # Assert
        assert result.success is False
        assert result.error == "Task not found"


class TestTaskServiceGetTasks:
    """Tests for task retrieval methods."""

    def test_get_task_by_id(self, task_service, mock_repository):
        """Test getting a task by ID."""
        # Arrange
        expected_task = TaskEntity(id=1, title="Test Task")
        mock_repository.get_by_id.return_value = expected_task

        # Act
        result = task_service.get_task(1)

        # Assert
        assert result is not None
        assert result.id == 1
        assert result.title == "Test Task"

    def test_get_all_active_tasks(self, task_service, mock_repository):
        """Test getting all active tasks."""
        # Arrange
        expected_tasks = [
            TaskEntity(id=1, title="Task 1"),
            TaskEntity(id=2, title="Task 2")
        ]
        mock_repository.get_all_active.return_value = expected_tasks

        # Act
        result = task_service.get_all_active_tasks()

        # Assert
        assert len(result) == 2
        assert all(isinstance(t, TaskEntity) for t in result)

    def test_get_completed_tasks_by_date(self, task_service, mock_repository):
        """Test getting completed tasks by date."""
        # Arrange
        expected_tasks = [TaskEntity(id=1, title="Completed Task")]
        mock_repository.get_completed_by_date.return_value = expected_tasks
        test_date = datetime(2026, 3, 30)

        # Act
        result = task_service.get_completed_tasks_by_date(test_date)

        # Assert
        assert len(result) == 1
        mock_repository.get_completed_by_date.assert_called_once_with(test_date)


class TestTaskServiceDateFormatting:
    """Tests for date formatting methods."""

    def test_format_date_for_display(self, task_service):
        """Test date formatting for display."""
        # Arrange
        test_date = datetime(2026, 3, 30)

        # Act
        result = task_service.format_date_for_display(test_date)

        # Assert
        assert result == "30 March 2026"

    def test_format_date_short(self, task_service):
        """Test short date formatting."""
        # Arrange
        test_date = datetime(2026, 3, 30)

        # Act
        result = task_service.format_date_short(test_date)

        # Assert
        assert result == "30/03"
