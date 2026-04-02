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

    This view shows all non-completed tasks grouped by date in a scrollable area
    with a quick-add button at the top.

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
        self._date_groups: dict[datetime, DateGroupWidget] = {}
        self._groups_layout: QVBoxLayout | None = None

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
        self._scroll_area.setObjectName("tasksScrollArea")
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Container for task widgets with date groups
        self._tasks_container = QWidget()
        self._groups_layout = QVBoxLayout(self._tasks_container)
        self._groups_layout.setContentsMargins(0, 0, 0, 0)
        self._groups_layout.setSpacing(8)
        self._groups_layout.addStretch()

        self._scroll_area.setWidget(self._tasks_container)
        layout.addWidget(self._scroll_area, 1)

        # Empty state label
        self._empty_label = QLabel("No active tasks. Add one above!")
        self._empty_label.setObjectName("emptyStateLabel")
        empty_font = QFont()
        empty_font.setPointSize(11)
        self._empty_label.setFont(empty_font)
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._groups_layout.addWidget(self._empty_label)

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
        for group in self._date_groups.values():
            group.deleteLater()
        self._task_widgets.clear()
        self._date_groups.clear()

    def _get_or_create_date_group(self, date_value: datetime) -> DateGroupWidget:
        """Get or create a date group widget.

        Args:
            date_value: Date for the group.

        Returns:
            DateGroupWidget: The date group widget.
        """
        if date_value not in self._date_groups:
            group = DateGroupWidget(date_value)
            group.set_expanded(False)  # Collapsed by default

            # Insert in chronological order (newest first)
            dates = sorted(self._date_groups.keys(), reverse=True)
            insert_index = 0
            for i, d in enumerate(dates):
                if date_value > d:
                    insert_index = i
                    break
                insert_index = i + 1

            self._groups_layout.insertWidget(insert_index, group)
            self._date_groups[date_value] = group

        return self._date_groups[date_value]

    def add_task(self, task: TaskEntity) -> None:
        """Add a task widget to the view.

        Args:
            task: Task entity to display.
        """
        # Remove empty state if present
        if self._empty_label:
            self._empty_label.setVisible(False)

        # Get or create date group based on created_at date
        created_date = task.created_at.date()
        date_key = datetime(created_date.year, created_date.month, created_date.day)
        group = self._get_or_create_date_group(date_key)

        # Create task widget
        task_widget = TaskItemWidget(
            task_id=task.id,  # type: ignore
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            completed_at=task.completed_at,
            show_checkbox=True
        )

        # Connect signals
        task_widget.checked.connect(self.toggle_requested.emit)
        task_widget.edit_requested.connect(self.edit_requested.emit)
        task_widget.delete_requested.connect(self.delete_requested.emit)
        task_widget.reopen_requested.connect(self.reopen_requested.emit)

        group.add_task_widget(task_widget)
        self._task_widgets[task.id] = task_widget  # type: ignore

        # Update count
        count = len([w for w in self._task_widgets.values()
                     if w._created_at and
                     w._created_at.date() == created_date])
        group.set_task_count(count)
        group.set_expanded(True)  # Expand when adding new task

    def set_tasks(self, tasks: list[TaskEntity]) -> None:
        """Set the tasks to display, grouped by date.

        Args:
            tasks: List of TaskEntity objects to display.
        """
        self.clear_tasks()

        # Group tasks by date
        tasks_by_date: dict[datetime, list[TaskEntity]] = {}
        for task in tasks:
            created_date = task.created_at.date()
            date_key = datetime(created_date.year, created_date.month, created_date.day)
            if date_key not in tasks_by_date:
                tasks_by_date[date_key] = []
            tasks_by_date[date_key].append(task)

        # Sort dates in reverse chronological order
        for date_value in sorted(tasks_by_date.keys(), reverse=True):
            date_tasks = tasks_by_date[date_value]
            if date_tasks:
                group = self._get_or_create_date_group(date_value)
                group.set_expanded(False)  # Collapsed by default

                for task in date_tasks:
                    task_widget = TaskItemWidget(
                        task_id=task.id,  # type: ignore
                        title=task.title,
                        description=task.description,
                        created_at=task.created_at,
                        completed_at=task.completed_at,
                        show_checkbox=True
                    )

                    task_widget.checked.connect(self.toggle_requested.emit)
                    task_widget.edit_requested.connect(self.edit_requested.emit)
                    task_widget.delete_requested.connect(self.delete_requested.emit)
                    task_widget.reopen_requested.connect(self.reopen_requested.emit)

                    group.add_task_widget(task_widget)
                    self._task_widgets[task.id] = task_widget  # type: ignore

                group.set_task_count(len(date_tasks))

        # Show/hide empty state
        if self._empty_label:
            self._empty_label.setVisible(len(self._task_widgets) == 0)

    def handle_operation_result(
            self,
            result: TaskServiceResult,
            operation: str,
            task_id: int | None = None
    ) -> None:
        """Handle the result of a task operation.

        Args:
            result: Result of the operation.
            operation: Type of operation ('create', 'toggle', 'delete').
            task_id: Optional task ID for toggle/delete operations.
        """
        if operation == 'create':
            if result.success and result.task:
                self.add_task(result.task)
        elif operation == 'toggle':
            if result.success and task_id in self._task_widgets:
                # Remove toggled task from view
                widget = self._task_widgets.pop(task_id)
                
                # Find and remove from date group
                created_date = widget._created_at.date()
                date_key = datetime(created_date.year, created_date.month, created_date.day)
                if date_key in self._date_groups:
                    group = self._date_groups[date_key]
                    group.remove_task_widget(task_id)
                    
                    # Remove empty group
                    if group._content_layout.count() == 0:
                        group.deleteLater()
                        del self._date_groups[date_key]
                
                widget.deleteLater()
                
                # Show empty state if no tasks
                if not self._task_widgets and self._empty_label:
                    self._empty_label.setVisible(True)
        elif operation == 'delete':
            if result.success and task_id in self._task_widgets:
                widget = self._task_widgets.pop(task_id)
                
                # Find and remove from date group
                created_date = widget._created_at.date()
                date_key = datetime(created_date.year, created_date.month, created_date.day)
                if date_key in self._date_groups:
                    group = self._date_groups[date_key]
                    group.remove_task_widget(task_id)
                    
                    # Remove empty group
                    if group._content_layout.count() == 0:
                        group.deleteLater()
                        del self._date_groups[date_key]
                
                widget.deleteLater()
                
                # Show empty state if no tasks
                if not self._task_widgets and self._empty_label:
                    self._empty_label.setVisible(True)
