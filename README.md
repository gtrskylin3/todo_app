# TODO Application

A robust, maintainable, and scalable Desktop TODO Application built with PyQt6 and SQLAlchemy.

## Features

- **Active Tasks View**: Manage daily tasks with Markdown-style checkboxes
- **Completed Tasks View**: Review history by completion date
- **Quick Add**: Add tasks quickly with the input field at the top
- **Edit/Delete**: Modify or remove tasks with confirmation dialogs
- **Dark Theme**: Modern dark UI with Qt Style Sheets
- **Background Operations**: All database operations run in separate threads to prevent UI freezing

## Technical Stack

- **Language**: Python 3.11+
- **Package Manager**: `uv`
- **GUI Framework**: PyQt6
- **ORM**: SQLAlchemy
- **Database**: SQLite
- **Testing**: pytest
- **Code Quality**: ruff, mypy

## Architecture

The application follows Clean Architecture principles:

```
src/
├── domain/           # Entities and business rules
├── infrastructure/   # Database and repository implementations
├── application/      # Use cases and services
├── presentation/     # PyQt UI components
└── config/           # Configuration and settings
```

### Design Patterns

- **Repository Pattern**: Abstracts data access from business logic
- **Dependency Injection**: Dependencies passed into services and views
- **Signal/Slot**: Qt's decoupled communication mechanism
- **Worker Threads**: QThread-based background operations

## Installation

### Prerequisites

- Python 3.11 or higher
- `uv` package manager

### Setup

1. **Install dependencies using uv**:

```bash
uv add pyqt6 sqlalchemy
uv add --dev pytest ruff mypy
```

2. **Run the application**:

```bash
uv run python main.py
```

## Usage

### Adding Tasks

1. Type a task title in the input field at the top
2. Press Enter or click "Add"

### Completing Tasks

1. Click the checkbox next to a task to mark it as completed
2. Completed tasks move to the "Completed" tab

### Editing Tasks

1. Click on a task title to expand its details
2. Click "Edit" to modify the title and description
3. Click "Save" to apply changes

### Deleting Tasks

1. Click on a task title to expand its details
2. Click "Remove" to delete the task
3. Confirm the deletion in the dialog

### Reopening Tasks

1. Go to the "Completed" tab
2. Click on a date to expand the list of completed tasks
3. Click "Reopen" on a task to move it back to active tasks

## Running Tests

```bash
uv run pytest tests/ -v
```

## Code Quality

### Linting with ruff

```bash
uv run ruff check src/ tests/
```

### Type checking with mypy

```bash
uv run mypy src/
```

## Project Structure

```
todo_app/
├── main.py                 # Application entry point
├── pyproject.toml          # Project configuration
├── TechSpec.md             # Technical specification
├── README.md               # This file
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py     # Application configuration
│   │   └── logging_config.py # Logging setup
│   ├── domain/
│   │   ├── __init__.py
│   │   └── task_entity.py  # Task domain entity
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── database.py # Database engine setup
│   │   │   └── models.py   # SQLAlchemy models
│   │   └── repositories/
│   │       ├── __init__.py
│   │       ├── abstract_repository.py # Repository interface
│   │       └── sqlalchemy_repository.py # Repository implementation
│   ├── application/
│   │   ├── __init__.py
│   │   └── task_service.py # Business logic service
│   └── presentation/
│       ├── __init__.py
│       ├── widgets/
│       │   ├── __init__.py
│       │   ├── task_item_widget.py    # Task display widget
│       │   ├── date_group_widget.py   # Date grouping widget
│       │   └── edit_task_dialog.py    # Edit dialog
│       ├── views/
│       │   ├── __init__.py
│       │   ├── active_tasks_view.py   # Active tasks view
│       │   ├── completed_tasks_view.py # Completed tasks view
│       │   └── main_window.py         # Main application window
│       └── workers/
│           ├── __init__.py
│           └── db_worker.py           # Background worker threads
└── tests/
    ├── __init__.py
    ├── test_task_entity.py    # Domain layer tests
    ├── test_repository.py     # Infrastructure layer tests
    └── test_task_service.py   # Application layer tests
```

## Configuration

The application can be configured via environment variables:

- `TODO_DB_PATH`: Path to the SQLite database file (default: `./data/todo.db`)
- `TODO_DB_ECHO`: Enable SQL echo for debugging (default: `false`)
- `TODO_LOG_PATH`: Path to the log file (default: `./logs/app.log`)
- `TODO_LOG_LEVEL`: Logging level (default: `INFO`)

## Logging

The application logs to both a file (`logs/app.log`) and the console. Log messages include:
- Application startup/shutdown
- Task operations (create, update, delete, toggle)
- Database errors

## License

This project is provided as-is for educational purposes.
