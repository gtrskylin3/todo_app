"""Unit tests for the TaskEntity domain object.

This module contains pytest tests for the domain layer,
testing the TaskEntity business logic and validation.
"""

from datetime import datetime

from src.domain.task_entity import TaskEntity


class TestTaskEntityCreation:
    """Tests for TaskEntity creation."""

    def test_create_task_with_defaults(self):
        """Test creating a task with default values."""
        # Act
        task = TaskEntity()

        # Assert
        assert task.id is None
        assert task.title == ""
        assert task.description is None
        assert task.is_completed is False
        assert task.completed_at is None

    def test_create_task_with_values(self):
        """Test creating a task with specific values."""
        # Arrange
        title = "Test Task"
        description = "Test Description"

        # Act
        task = TaskEntity(title=title, description=description)

        # Assert
        assert task.title == title
        assert task.description == description
        assert task.is_completed is False


class TestTaskEntityCompletion:
    """Tests for task completion functionality."""

    def test_mark_completed(self):
        """Test marking a task as completed."""
        # Arrange
        task = TaskEntity(title="Test")
        assert task.is_completed is False

        # Act
        task.mark_completed()

        # Assert
        assert task.is_completed is True
        assert task.completed_at is not None

    def test_mark_completed_twice(self):
        """Test marking an already completed task."""
        # Arrange
        task = TaskEntity(title="Test")
        task.mark_completed()
        first_completion = task.completed_at

        # Act
        task.mark_completed()

        # Assert
        assert task.is_completed is True
        assert task.completed_at == first_completion  # Should not change

    def test_mark_incomplete(self):
        """Test marking a completed task as incomplete."""
        # Arrange
        task = TaskEntity(title="Test")
        task.mark_completed()
        assert task.is_completed is True

        # Act
        task.mark_incomplete()

        # Assert
        assert task.is_completed is False
        assert task.completed_at is None

    def test_mark_incomplete_on_incomplete_task(self):
        """Test marking an already incomplete task."""
        # Arrange
        task = TaskEntity(title="Test")

        # Act
        task.mark_incomplete()

        # Assert
        assert task.is_completed is False
        assert task.completed_at is None


class TestTaskEntityDateFormatting:
    """Tests for date formatting methods."""

    def test_get_completion_date_str_completed(self):
        """Test getting completion date string for completed task."""
        # Arrange
        task = TaskEntity(title="Test")
        task.completed_at = datetime(2026, 3, 30, 14, 30)

        # Act
        result = task.get_completion_date_str()

        # Assert
        assert result == "30/03"

    def test_get_completion_date_str_incomplete(self):
        """Test getting completion date string for incomplete task."""
        # Arrange
        task = TaskEntity(title="Test")

        # Act
        result = task.get_completion_date_str()

        # Assert
        assert result == ""

    def test_get_created_date_str(self):
        """Test getting created date string."""
        # Arrange
        created_at = datetime(2026, 3, 30, 14, 30)
        task = TaskEntity(title="Test", created_at=created_at)

        # Act
        result = task.get_created_date_str()

        # Assert
        assert result == "30/03/2026"

    def test_get_created_time_str(self):
        """Test getting created time string."""
        # Arrange
        created_at = datetime(2026, 3, 30, 14, 30)
        task = TaskEntity(title="Test", created_at=created_at)

        # Act
        result = task.get_created_time_str()

        # Assert
        assert result == "14:30"


class TestTaskEntityValidation:
    """Tests for task validation."""

    def test_validate_valid_task(self):
        """Test validating a valid task."""
        # Arrange
        task = TaskEntity(title="Valid Task")

        # Act
        is_valid, error = task.validate()

        # Assert
        assert is_valid is True
        assert error is None

    def test_validate_empty_title(self):
        """Test validating a task with empty title."""
        # Arrange
        task = TaskEntity(title="")

        # Act
        is_valid, error = task.validate()

        # Assert
        assert is_valid is False
        assert error == "Task title cannot be empty"

    def test_validate_whitespace_title(self):
        """Test validating a task with whitespace-only title."""
        # Arrange
        task = TaskEntity(title="   ")

        # Act
        is_valid, error = task.validate()

        # Assert
        assert is_valid is False
        assert error == "Task title cannot be empty"

    def test_validate_title_too_long(self):
        """Test validating a task with title exceeding 200 characters."""
        # Arrange
        task = TaskEntity(title="A" * 201)

        # Act
        is_valid, error = task.validate()

        # Assert
        assert is_valid is False
        assert error == "Task title must not exceed 200 characters"

    def test_validate_title_exactly_200_chars(self):
        """Test validating a task with title of exactly 200 characters."""
        # Arrange
        task = TaskEntity(title="A" * 200)

        # Act
        is_valid, error = task.validate()

        # Assert
        assert is_valid is True
        assert error is None

    def test_validate_with_description(self):
        """Test validating a task with description."""
        # Arrange
        task = TaskEntity(
            title="Valid Task",
            description="A" * 1000  # Long description should be fine
        )

        # Act
        is_valid, error = task.validate()

        # Assert
        assert is_valid is True
        assert error is None


class TestTaskEntityProperties:
    """Tests for TaskEntity properties."""

    def test_is_completed_false(self):
        """Test is_completed property when task is incomplete."""
        # Arrange
        task = TaskEntity(title="Test")

        # Assert
        assert task.is_completed is False

    def test_is_completed_true(self):
        """Test is_completed property when task is complete."""
        # Arrange
        task = TaskEntity(title="Test")
        task.completed_at = datetime.now()

        # Assert
        assert task.is_completed is True

    def test_is_completed_with_none_completed_at(self):
        """Test is_completed property with None completed_at."""
        # Arrange
        task = TaskEntity(title="Test", completed_at=None)

        # Assert
        assert task.is_completed is False
