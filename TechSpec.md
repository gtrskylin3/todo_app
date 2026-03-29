# Role
Act as a Senior Python Architect and Desktop Application Developer. You are an expert in PyQt6, SQLAlchemy, Clean Architecture, and Design Patterns.

# Project Overview
Develop a robust, maintainable, and scalable Desktop TODO Application. The application allows users to manage daily tasks, mark them as completed, and review history by date. The application must separate business logic from the UI layer strictly.

# Technical Stack
- **Language:** Python 3.11+
- **Package Manager:** `uv` (include `pyproject.toml`)
- **GUI Framework:** PyQt6
- **ORM:** SQLAlchemy (Async or Sync, but DB operations must not block the UI thread)
- **Database:** SQLite
- **Testing:** pytest
- **Code Quality:** ruff, mypy

# Architecture & Design Patterns
1.  **Clean Architecture / Layered Architecture:**
    -   `domain/`: Entities and Business Rules.
    -   `infrastructure/`: Database implementation, Repository implementations.
    -   `presentation/`: PyQt UI, Widgets, Views.
    -   `application/`: Use Cases / Services (orchestrates domain and infrastructure).
2.  **Repository Pattern:** Abstract the data access layer. The UI must never interact with SQLAlchemy directly.
3.  **Dependency Injection:** Pass dependencies (repositories, services) into ViewModels or Controllers.
4.  **Signal/Slot Decoupling:** UI components should communicate via Qt Signals/Slots, not direct method calls where possible.
5.  **Threading:** All database operations must run in a separate thread (`QThread` or `QRunnable`) to prevent UI freezing.

# Data Model (Task Entity)
The `Task` entity must contain:
-   `id`: Integer, Primary Key
-   `title`: String (required, max 200 chars)
-   `description`: String (optional, text)
-   `created_at`: DateTime (auto-generated)
-   `completed_at`: DateTime (nullable, set when task is completed)
-   `is_completed`: Boolean (computed property based on `completed_at`)

# Functional Requirements

## 1. Active Tasks View (Default)
-   Display a list of non-completed tasks.
-   **Visual Style:** Tasks should resemble Markdown checkboxes.
    -   Format: `[ ] Task Title [DD/MM]`
    -   If completed: `[x] Task Title [DD/MM]` (moves to Completed View).
-   **Interaction:**
    -   Clicking the Checkbox: Toggles completion status immediately.
    -   Clicking the Title: Expands/Collapses an accordion-style section below the title.
    -   **Expanded Section:** Shows `description`, `created_at`, and action buttons `[Edit]`, `[Remove]`.
-   **Create Task:** A prominent input field at the top to add new tasks quickly.

## 2. Completed Tasks View (Tab/Section)
-   Display a list of dates in reverse chronological order (e.g., "25 March 2026", "24 March 2026").
-   **Interaction:**
    -   Clicking a Date header expands to show the list of tasks completed on that specific day.
    -   Tasks in this view are read-only (or allow "Reopen" functionality).

## 3. Task Management
-   **Create:** Validate title is not empty.
-   **Edit:** Open a dialog or inline editor to modify title and description.
-   **Delete:** Soft delete or hard delete (prefer hard delete for simplicity, with confirmation dialog).
-   **Persistence:** All changes must be saved to SQLite immediately.

# Code Quality & Best Practices
1.  **Type Hinting:** Full type annotations for all functions and class attributes.
2.  **Docstrings:** Google or NumPy style docstrings for all classes and public methods.
3.  **Comments:** Explain *why* complex logic exists, not *what* the code does.
4.  **Error Handling:** Graceful handling of DB errors. Show user-friendly QMessageBox on critical failures.
5.  **Logging:** Configure `logging` module to write to a file (`app.log`) and console.
6.  **Styling:** Use Qt Style Sheets (QSS) for a modern, clean look. Do not rely on default OS styling.
7.  **Configuration:** Use a config file or environment variables for DB path and app settings.

# Implementation Plan (Step-by-Step)
Please implement the solution following these steps. Do not skip steps.

### Step 1: Project Initialization
-   Create `pyproject.toml` with dependencies (`pyqt6`, `sqlalchemy`, `pytest`, etc.).
-   Set up the directory structure (`src/domain`, `src/infrastructure`, `src/presentation`, etc.).
-   Configure logging and basic app entry point (`main.py`).

### Step 2: Database & Domain Layer
-   Define the `Task` SQLAlchemy model.
-   Create the `TaskEntity` dataclass (pure python object for domain logic).
-   Initialize the SQLite database engine.

### Step 3: Repository Pattern
-   Create an abstract base class `AbstractTaskRepository`.
-   Implement `SqlalchemyTaskRepository` inheriting from the abstract class.
-   Define methods: `add`, `get_all_active`, `get_completed_by_date`, `update`, `delete`, `toggle_completion`.

### Step 4: Application Services
-   Create a `TaskService` class that uses the Repository.
-   Implement business logic (e.g., validation, date formatting).
-   Ensure this layer is UI-agnostic.

### Step 5: UI Components (Widgets)
-   Create a custom `TaskItemWidget` (QFrame) that implements the Markdown-style look.
    -   Handle expand/collapse logic.
    -   Emit signals: `checked`, `edit_requested`, `delete_requested`.
-   Create a `DateGroupWidget` for the Completed Tasks view.

### Step 6: Main Window & Integration
-   Create the `MainWindow` with tabs (Active, Completed).
-   Implement a `Worker` thread class for DB operations to keep UI responsive.
-   Connect Services to UI via Signals/Slots.

### Step 7: Testing & Polish
-   Write `pytest` unit tests for the Service and Repository layers.
-   Add QSS styling for a modern dark/light mode aesthetic.
-   Verify all docstrings and type hints are present.

# Deliverables
1.  Full source code structure.
2.  `pyproject.toml` configuration.
3.  Instructions on how to run the app using `uv`.

# Constraint
-   Use "uv add" for install python packages
-   Do not put business logic inside UI classes.
-   Do not block the main thread during DB I/O.
-   Ensure the code is production-ready, not a prototype.