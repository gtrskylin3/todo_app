# TODO Application

A modern, dark-themed Desktop TODO Application built with PyQt6 and SQLAlchemy.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 📖 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Architecture](#-architecture)
- [Development](#-development)
- [Troubleshooting](#-troubleshooting)

---

## ✨ Features

### Core Functionality

- ✅ **Active Tasks View** — Manage daily tasks with Markdown-style checkboxes
- ✅ **Completed Tasks View** — Review history organized by completion date
- ✅ **Quick Add** — Add tasks with Enter key from the top input field
- ✅ **Edit Tasks** — Modify task title and description via dialog
- ✅ **Delete Tasks** — Remove tasks with confirmation dialog
- ✅ **Task Completion** — Click checkbox to mark tasks as done
- ✅ **Date Grouping** — Completed tasks grouped by date (reverse chronological)

### UI/UX

- 🎨 **Dark Theme** — Obsidian × Spotify inspired design
- 🎨 **Modern Styling** — Purple accent colors (#8B5CF6)
- 🎨 **Smooth Interactions** — Hover effects and transitions
- 🎨 **No UI Blocking** — All database operations run in background threads
- 🎨 **Clean Layout** — Minimal design with focus on content

### Technical

- 🏗️ **Clean Architecture** — Domain ↔ Infrastructure ↔ Presentation layers
- 🏗️ **Repository Pattern** — Abstracted data access layer
- 🏗️ **Dependency Injection** — Explicit dependency management
- 🏗️ **Type Hints** — Full type annotations throughout
- 🏗️ **Comprehensive Tests** — 63 unit tests covering core logic

---

## 📸 Screenshots

### Active Tasks View
```
┌────────────────────────────────────────────┐
│  Active Tasks                       [⚙]   │
├────────────────────────────────────────────┤
│  [Add a new task... Press Enter]  [Add]   │
├────────────────────────────────────────────┤
│  ☐ Task Title 1              [15/03]      │
│  ☐ Task Title 2              [14/03]      │
│  ☑ Completed Task              [13/03]    │
└────────────────────────────────────────────┘
```

### Completed Tasks View
```
┌────────────────────────────────────────────┐
│  Completed Tasks                    [⚙]   │
├────────────────────────────────────────────┤
│  ▼ 15 March 2026                  (3)     │
│    ☑ Task A  ☑ Task B  ☑ Task C           │
├────────────────────────────────────────────┤
│  ▶ 14 March 2026                  (2)     │
└────────────────────────────────────────────┘
```

---

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- `uv` package manager

### Step 1: Install uv (if not installed)

```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 2: Clone and Setup

```bash
# Navigate to project directory
cd todo_app

# Install dependencies
uv add pyqt6 sqlalchemy
uv add --dev pytest ruff mypy
```

### Step 3: Verify Installation

```bash
# Run tests
uv run pytest tests/ -v

# Run linter
uv run ruff check src/
```

---

## 🚀 Usage

### Running the Application

```bash
# Using uv
uv run python main.py

# Or activate virtual environment first
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
python main.py
```

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Enter` (in input) | Add new task |
| `Ctrl+Q` | Exit application |
| `Ctrl+,` | Open Settings |

### Task Management

#### Creating Tasks
1. Type task title in the input field at the top
2. Press `Enter` or click "Add"
3. Task appears in the Active Tasks list

#### Completing Tasks
1. Click the checkbox next to a task
2. Task moves to Completed tab automatically
3. Completion date is recorded

#### Editing Tasks
1. Click on task title to expand details
2. Click "Edit" button
3. Modify title/description in dialog
4. Click "Save"

#### Deleting Tasks
1. Click on task title to expand details
2. Click "Remove" button
3. Confirm deletion in dialog

#### Reopening Tasks
1. Go to "Completed" tab
2. Click on a date to expand (if collapsed)
3. Click "Reopen" on the task
4. Task returns to Active tab

---

## 📁 Project Structure

```
todo_app/
├── main.py                      # Application entry point
├── pyproject.toml               # Project dependencies
├── README.md                    # This file
├── TechSpec.md                  # Technical specification
├── DESIGN.md                    # Design system guide
├── start.bat                    # Windows launcher script
├── .venv/                       # Virtual environment
├── data/                        # SQLite database storage
│   └── todo.db
├── logs/                        # Application logs
│   └── app.log
├── src/
│   ├── config/
│   │   ├── settings.py          # App configuration
│   │   └── logging_config.py    # Logging setup
│   ├── domain/
│   │   └── task_entity.py       # Task business entity
│   ├── infrastructure/
│   │   ├── db/
│   │   │   ├── database.py      # SQLAlchemy engine
│   │   │   └── models.py        # ORM models
│   │   └── repositories/
│   │       ├── abstract_repository.py
│   │       └── sqlalchemy_repository.py
│   ├── application/
│   │   └── task_service.py      # Business logic
│   └── presentation/
│       ├── styles.py            # Centralized QSS styles
│       ├── widgets/
│       │   ├── task_item_widget.py
│       │   ├── date_group_widget.py
│       │   └── edit_task_dialog.py
│       ├── views/
│       │   ├── active_tasks_view.py
│       │   ├── completed_tasks_view.py
│       │   └── main_window.py
│       └── workers/
│           └── db_worker.py     # Background threads
└── tests/
    ├── test_task_entity.py      # Domain layer tests
    ├── test_repository.py       # Infrastructure tests
    └── test_task_service.py     # Application tests
```

---

## 🏛️ Architecture

### Clean Architecture Layers

```
┌─────────────────────────────────────────────────┐
│              PRESENTATION LAYER                 │
│  (PyQt6 UI, Widgets, Views, Workers)            │
├─────────────────────────────────────────────────┤
│              APPLICATION LAYER                  │
│  (TaskService - Business Logic)                 │
├─────────────────────────────────────────────────┤
│              DOMAIN LAYER                       │
│  (TaskEntity - Pure Business Objects)           │
├─────────────────────────────────────────────────┤
│              INFRASTRUCTURE LAYER               │
│  (SQLAlchemy, Repositories, Database)           │
└─────────────────────────────────────────────────┘
```

### Design Patterns

| Pattern | Usage |
|---------|-------|
| **Repository** | Abstracts database access from business logic |
| **Dependency Injection** | Dependencies passed into services/views |
| **Signal/Slot** | Qt's decoupled communication |
| **Worker Thread** | Background DB operations (QThread) |
| **Service Layer** | Orchestrates domain + infrastructure |

---

## 🛠️ Development

### Running Tests

```bash
# All tests
uv run pytest tests/ -v

# With coverage
uv run pytest tests/ -v --cov=src

# Specific test file
uv run pytest tests/test_task_service.py -v
```

### Code Quality

```bash
# Linting
uv run ruff check src/ tests/

# Type checking
uv run mypy src/

# Auto-fix
uv run ruff check src/ tests/ --fix
```

### Adding New Features

1. **Domain Layer** — Create/update entities in `src/domain/`
2. **Infrastructure** — Add repository methods in `src/infrastructure/`
3. **Application** — Implement business logic in `src/application/`
4. **Presentation** — Create UI components in `src/presentation/`
5. **Tests** — Add tests in `tests/`

---

### Getting Help

- Check `logs/app.log` for error messages
- Run with debug logging: `TODO_LOG_LEVEL=DEBUG uv run python main.py`
- Open an issue on GitHub with error details

---
# 🔮 Future Plans — TODO Application

This document outlines planned features and improvements for future releases.

---

## 📋 Roadmap

### Version 1.1.0 — Settings & Customization *(Next Release)*

- [ ] **Settings Dialog**
  - [ ] Minimize to system tray toggle
  - [ ] Close to tray toggle
  - [ ] Custom background image selection
  - [ ] Window opacity slider (50-100%)
  - [ ] Settings persistence (JSON)

- [ ] **System Tray Integration**
  - [ ] Tray icon with context menu
  - [ ] Double-click to restore
  - [ ] Notification support

- [ ] **UI Improvements**
  - [ ] Settings button next to tabs
  - [ ] About button in bottom-right corner
  - [ ] Hidden menu bar

---

### Version 1.2.0 — Task Enhancements

- [ ] **Task Priorities**
  - [ ] Low/Medium/High priority levels
  - [ ] Color-coded priority indicators
  - [ ] Filter by priority

- [ ] **Task Categories/Tags**
  - [ ] Create custom categories
  - [ ] Assign tags to tasks
  - [ ] Filter by category/tag

- [ ] **Due Dates**
  - [ ] Set due date for tasks
  - [ ] Overdue task highlighting
  - [ ] Sort by due date

- [ ] **Task Search**
  - [ ] Search by title/description
  - [ ] Real-time filtering
  - [ ] Search highlights

---