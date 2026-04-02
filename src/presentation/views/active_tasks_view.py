"""View for displaying active (non-completed) tasks.

This module provides the ActiveTasksView which shows all non-completed
tasks grouped by date with a quick-add button at the top.
"""

from datetime import datetime
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.application.task_service import TaskServiceResult
from src.domain.task_entity import TaskEntity
from src.presentation.styles import get_active_tasks_view_styles
from src.presentation.widgets.create_task_dialog import CreateTaskDialog
from src.presentation.widgets.date_group_widget import DateGroupWidget
from src.presentation.widgets.task_item_widget import TaskItemWidget


class ActiveTasksView(QWidget):
    """View for displaying and managing active tasks.
    
    This view shows all non-completed tasks in a scrollable area
    with a quick-add input field at the top.
    
    Signals:
        create_requested: Emitted when a new task should be created (title: str, description: str | None).
        toggle_requested: Emitted when task completion should be toggled (task_id: int).
        edit_requested: Emitted when task edit is requested (task_id: int).
        delete_requested: Emitted when task deletion is requested (task_id: int).
    """

    create_requested = pyqtSignal(str, str)  # title, description
    toggle_requested = pyqtSignal(int)
    edit_requested = pyqtSignal(int)
    delete_requested = pyqtSignal(int)
    reopen_requested = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None):
        """Initialize the active tasks view.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setObjectName("activeTasksView")

        self._task_widgets: dict[int, TaskItemWidget] = {}

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header_label = QLabel("Active Tasks")
        header_label.setObjectName("headerLabel")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setWeight(QFont.Weight.Bold)
        header_label.setFont(header_font)
        layout.addWidget(header_label)

        # Add button
        add_layout = QHBoxLayout()
        add_btn = QPushButton("+ Add New Task")
        add_btn.setObjectName("addButton")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setFixedHeight(40)
        add_btn.clicked.connect(self._on_add_clicked)
        add_layout.addWidget(add_btn)
        add_layout.addStretch()

        layout.addLayout(add_layout)

        # Scroll area for tasks
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Container for task widgets
        self._tasks_container = QWidget()
        self._tasks_layout = QVBoxLayout(self._tasks_container)
        self._tasks_layout.setContentsMargins(0, 0, 0, 0)
        self._tasks_layout.setSpacing(8)
        self._tasks_layout.addStretch()

        self._scroll_area.setWidget(self._tasks_container)
    
        layout.addWidget(self._scroll_area)

        # Empty state label
        self._empty_label = QLabel("No active tasks. Add one above!")
        self._empty_label.setObjectName("emptyStateLabel")
        empty_font = QFont()
        empty_font.setPointSize(11)
        self._empty_label.setFont(empty_font)
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._tasks_layout.addWidget(self._empty_label)

    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets for modern appearance."""
        self.setStyleSheet(get_active_tasks_view_styles())

    def _on_add_clicked(self) -> None:
        """Handle add button click."""
        dialog = CreateTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            title, description = dialog.get_result()
            if title:
                self.create_requested.emit(title, description or "")

    def clear_tasks(self) -> None:
        """Clear all task widgets from the view."""
        for widget in self._task_widgets.values():
            widget.deleteLater()
        self._task_widgets.clear()

    def add_task(self, task: TaskEntity) -> None:
        """Add a task widget to the view.
        
        Args:
            task: Task entity to display.
        """
        # Remove empty state if present
        if self._empty_label:
            self._empty_label.setVisible(False)

        # Create task widget
        task_widget = TaskItemWidget(
            task_id=task.id,  # type: ignore
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            completed_at=task.completed_at
        )

        # Connect signals
        task_widget.checked.connect(self._on_task_checked)
        task_widget.edit_requested.connect(self.edit_requested.emit)
        task_widget.delete_requested.connect(self.delete_requested.emit)
        task_widget.reopen_requested.connect(self.reopen_requested.emit)

        # Add to layout and dictionary
        self._tasks_layout.insertWidget(0, task_widget)
        self._task_widgets[task.id] = task_widget  # type: ignore

    def remove_task(self, task_id: int) -> None:
        """Remove a task widget from the view.
        
        Args:
            task_id: ID of the task to remove.
        """
        if task_id in self._task_widgets:
            widget = self._task_widgets.pop(task_id)
            widget.deleteLater()

            # Show empty state if no tasks
            if not self._task_widgets:
                self._empty_label.setVisible(True)

    def update_task_completion(self, task_id: int, is_completed: bool) -> None:
        """Update a task's completion status.
        
        Args:
            task_id: ID of the task to update.
            is_completed: Whether the task is completed.
        """
        if task_id in self._task_widgets:
            self._task_widgets[task_id].update_completion_status(is_completed)

    def _on_task_checked(self, task_id: int) -> None:
        """Handle task checkbox toggle.
        
        Args:
            task_id: ID of the task that was toggled.
        """
        self.toggle_requested.emit(task_id)

    def set_tasks(self, tasks: list[TaskEntity]) -> None:
        """Set the list of tasks to display.
        
        Args:
            tasks: List of task entities to display.
        """
        self.clear_tasks()
        for task in tasks:
            self.add_task(task)

    def handle_operation_result(self, result: TaskServiceResult,
                                 operation: str, task_id: int | None = None) -> None:
        """Handle the result of a task operation.
        
        Args:
            result: Result of the operation.
            operation: Type of operation ('create', 'toggle', 'delete', 'reopen').
            task_id: Optional task ID for the operation.
        """
        if operation == 'create':
            if result.success and result.task:
                self.add_task(result.task)
        elif operation == 'toggle':
            if result.success and task_id:
                if result.task and result.task.is_completed:
                    self.remove_task(task_id)
                else:
                    self.update_task_completion(task_id, False)
        elif operation == 'delete':
            if result.success and task_id:
                self.remove_task(task_id)
        elif operation == 'reopen':
            if result.success and task_id and result.task:
                self.remove_task(task_id)
                self.add_task(result.task)
