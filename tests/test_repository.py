"""Unit tests for the SQLAlchemy task repository.

This module contains pytest tests for the infrastructure layer,
testing database operations with an in-memory SQLite database.
"""

from datetime import datetime, timedelta

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.domain.task_entity import TaskEntity
from src.infrastructure.db.database import Base
from src.infrastructure.db.models import TaskModel
from src.infrastructure.repositories.sqlalchemy_repository import SQLAlchemyTaskRepository


@pytest.fixture
def in_memory_engine():
    """Create an in-memory SQLite database engine."""
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        future=True
    )
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(in_memory_engine):
    """Create a session factory for the in-memory database."""
    return sessionmaker(
        bind=in_memory_engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False
    )


@pytest.fixture
def repository(session_factory):
    """Create a repository instance with in-memory database."""
    return SQLAlchemyTaskRepository(session_factory)


@pytest.fixture
def sample_task():
    """Create a sample task entity."""
    return TaskEntity(
        title="Test Task",
        description="Test Description"
    )


class TestRepositoryAdd:
    """Tests for repository add method."""

    def test_add_task(self, repository, sample_task):
        """Test adding a task to the repository."""
        # Act
        result = repository.add(sample_task)

        # Assert
        assert result.id is not None
        assert result.title == "Test Task"
        assert result.description == "Test Description"
        assert result.is_completed is False

    def test_add_task_generates_id(self, repository, sample_task):
        """Test that adding a task generates an auto-increment ID."""
        # Act
        task1 = repository.add(sample_task)
        task2 = repository.add(sample_task)

        # Assert
        assert task1.id is not None
        assert task2.id is not None
        assert task1.id < task2.id


class TestRepositoryGetById:
    """Tests for repository get_by_id method."""

    def test_get_existing_task(self, repository, sample_task):
        """Test getting an existing task by ID."""
        # Arrange
        added_task = repository.add(sample_task)

        # Act
        result = repository.get_by_id(added_task.id)  # type: ignore

        # Assert
        assert result is not None
        assert result.id == added_task.id
        assert result.title == sample_task.title

    def test_get_nonexistent_task(self, repository):
        """Test getting a non-existent task."""
        # Act
        result = repository.get_by_id(999)

        # Assert
        assert result is None


class TestRepositoryGetAllActive:
    """Tests for repository get_all_active method."""

    def test_get_all_active_empty(self, repository):
        """Test getting active tasks when none exist."""
        # Act
        result = repository.get_all_active()

        # Assert
        assert result == []

    def test_get_all_active_with_tasks(self, repository):
        """Test getting all active tasks."""
        # Arrange
        repository.add(TaskEntity(title="Active Task 1"))
        repository.add(TaskEntity(title="Active Task 2"))

        # Act
        result = repository.get_all_active()

        # Assert
        assert len(result) == 2
        assert all(not t.is_completed for t in result)

    def test_get_all_active_excludes_completed(self, repository):
        """Test that active tasks exclude completed tasks."""
        # Arrange
        repository.add(TaskEntity(title="Active Task"))
        completed_task = repository.add(TaskEntity(title="Completed Task"))
        repository.toggle_completion(completed_task.id)  # type: ignore

        # Act
        result = repository.get_all_active()

        # Assert
        assert len(result) == 1
        assert result[0].title == "Active Task"


class TestRepositoryToggleCompletion:
    """Tests for repository toggle_completion method."""

    def test_toggle_incomplete_to_complete(self, repository, sample_task):
        """Test toggling an incomplete task to complete."""
        # Arrange
        task = repository.add(sample_task)
        assert task.is_completed is False

        # Act
        result = repository.toggle_completion(task.id)  # type: ignore

        # Assert
        assert result is not None
        assert result.is_completed is True
        assert result.completed_at is not None

    def test_toggle_complete_to_incomplete(self, repository, sample_task):
        """Test toggling a complete task to incomplete."""
        # Arrange
        task = repository.add(sample_task)
        repository.toggle_completion(task.id)  # type: ignore
        assert task.is_completed is False  # Original entity not updated

        # Act
        result = repository.toggle_completion(task.id)  # type: ignore

        # Assert
        assert result is not None
        assert result.is_completed is False
        assert result.completed_at is None

    def test_toggle_nonexistent_task(self, repository):
        """Test toggling a non-existent task."""
        # Act
        result = repository.toggle_completion(999)

        # Assert
        assert result is None


class TestRepositoryReopen:
    """Tests for repository reopen method."""

    def test_reopen_completed_task(self, repository, sample_task):
        """Test reopening a completed task."""
        # Arrange
        task = repository.add(sample_task)
        repository.toggle_completion(task.id)  # type: ignore

        # Act
        result = repository.reopen(task.id)  # type: ignore

        # Assert
        assert result is not None
        assert result.is_completed is False
        assert result.completed_at is None

    def test_reopen_nonexistent_task(self, repository):
        """Test reopening a non-existent task."""
        # Act
        result = repository.reopen(999)

        # Assert
        assert result is None


class TestRepositoryUpdate:
    """Tests for repository update method."""

    def test_update_task(self, repository, sample_task):
        """Test updating a task."""
        # Arrange
        task = repository.add(sample_task)
        task.title = "Updated Title"
        task.description = "Updated Description"

        # Act
        result = repository.update(task)

        # Assert
        assert result.title == "Updated Title"
        assert result.description == "Updated Description"

    def test_update_nonexistent_task(self, repository):
        """Test updating a non-existent task."""
        # Arrange
        task = TaskEntity(id=999, title="Test")

        # Act & Assert
        with pytest.raises(ValueError):
            repository.update(task)


class TestRepositoryDelete:
    """Tests for repository delete method."""

    def test_delete_existing_task(self, repository, sample_task):
        """Test deleting an existing task."""
        # Arrange
        task = repository.add(sample_task)

        # Act
        result = repository.delete(task.id)  # type: ignore

        # Assert
        assert result is True
        assert repository.get_by_id(task.id) is None  # type: ignore

    def test_delete_nonexistent_task(self, repository):
        """Test deleting a non-existent task."""
        # Act
        result = repository.delete(999)

        # Assert
        assert result is False


class TestRepositoryGetCompletedByDate:
    """Tests for repository get_completed_by_date method."""

    def test_get_completed_by_date_empty(self, repository):
        """Test getting completed tasks for a date with none."""
        # Arrange
        test_date = datetime.now()

        # Act
        result = repository.get_completed_by_date(test_date)

        # Assert
        assert result == []

    def test_get_completed_by_date_with_tasks(self, repository):
        """Test getting completed tasks for a specific date."""
        # Arrange
        task1 = repository.add(TaskEntity(title="Task 1"))
        task2 = repository.add(TaskEntity(title="Task 2"))
        repository.toggle_completion(task1.id)  # type: ignore
        repository.toggle_completion(task2.id)  # type: ignore

        # Act
        result = repository.get_completed_by_date(datetime.now())

        # Assert
        assert len(result) == 2
        assert all(t.is_completed for t in result)

    def test_get_completed_by_date_filters_correctly(self, repository):
        """Test that get_completed_by_date filters by date correctly."""
        # Arrange
        task = repository.add(TaskEntity(title="Task"))
        repository.toggle_completion(task.id)  # type: ignore

        # Act - query for a different date
        different_date = datetime.now() - timedelta(days=7)
        result = repository.get_completed_by_date(different_date)

        # Assert
        assert result == []


class TestRepositoryGetAllCompletedDates:
    """Tests for repository get_all_completed_dates method."""

    def test_get_all_completed_dates_empty(self, repository):
        """Test getting completed dates when no tasks are completed."""
        # Arrange
        repository.add(TaskEntity(title="Active Task"))

        # Act
        result = repository.get_all_completed_dates()

        # Assert
        assert result == []

    def test_get_all_completed_dates_with_tasks(self, repository):
        """Test getting completed dates with completed tasks."""
        # Arrange
        task1 = repository.add(TaskEntity(title="Task 1"))
        task2 = repository.add(TaskEntity(title="Task 2"))
        repository.toggle_completion(task1.id)  # type: ignore
        repository.toggle_completion(task2.id)  # type: ignore

        # Act
        result = repository.get_all_completed_dates()

        # Assert
        assert len(result) > 0

    def test_get_all_completed_dates_returns_unique_dates(self, repository):
        """Test that completed dates are unique."""
        # Arrange
        task1 = repository.add(TaskEntity(title="Task 1"))
        task2 = repository.add(TaskEntity(title="Task 2"))
        repository.toggle_completion(task1.id)  # type: ignore
        repository.toggle_completion(task2.id)  # type: ignore

        # Act
        result = repository.get_all_completed_dates()

        # Assert - should have unique dates
        unique_dates = set(d.date() for d in result)
        assert len(result) == len(unique_dates)


class TestTaskEntityToModel:
    """Tests for TaskModel entity conversion."""

    def test_to_entity(self, in_memory_engine, sample_task):
        """Test converting model to entity."""
        # Arrange
        session_factory = sessionmaker(bind=in_memory_engine)
        session = session_factory()
        model = TaskModel.from_entity(sample_task)
        session.add(model)
        session.commit()
        session.refresh(model)

        # Act
        entity = model.to_entity()

        # Assert
        assert entity.id == model.id
        assert entity.title == model.title
        assert entity.description == model.description

    def test_from_entity(self, sample_task):
        """Test converting entity to model."""
        # Act
        model = TaskModel.from_entity(sample_task)

        # Assert
        assert model.title == sample_task.title
        assert model.description == sample_task.description
        assert model.is_completed == sample_task.is_completed
