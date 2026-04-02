"""View for displaying today's tasks.

This module provides the TodayTasksView which shows tasks created today
with a quick-add button at the top.
"""

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
from src.presentation.widgets.task_item_widget import TaskItemWidget


class TodayTasksView(QWidget):
    """View for displaying and managing today's tasks.

    This view shows tasks created today in a scrollable area
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
        """Initialize the today tasks view.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setObjectName("todayTasksView")

        self._task_widgets: dict[int, TaskItemWidget] = {}

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header_label = QLabel("Today's Tasks")
        header_label.setObjectName("headerLabel")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setWeight(QFont.Weight.Bold)
        header_label.setFont(header_font)
        layout.addWidget(header_label)

        # Add button
        add_layout = QHBoxLayout()
        self._add_button = QPushButton("+ Add New Task")
        self._add_button.setObjectName("addButton")
        self._add_button.setFixedHeight(40)
        self._add_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self._add_button.clicked.connect(self._on_add_button_clicked)
        add_layout.addWidget(self._add_button)
        add_layout.addStretch()
        layout.addLayout(add_layout)

        # Scroll area for tasks
        self._scroll_area = QScrollArea()
        self._scroll_area.setObjectName("tasksScrollArea")
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Content widget for scroll area
        self._scroll_content = QWidget()
        self._scroll_content.setObjectName("scrollContent")
        self._scroll_layout = QVBoxLayout(self._scroll_content)
        self._scroll_layout.setContentsMargins(0, 0, 0, 0)
        self._scroll_layout.setSpacing(8)
        self._scroll_layout.addStretch()

        self._scroll_area.setWidget(self._scroll_content)
        layout.addWidget(self._scroll_area, 1)

    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets."""
        self.setStyleSheet(get_active_tasks_view_styles(custom_background=False))

    def _on_add_button_clicked(self) -> None:
        """Handle add button click."""
        dialog = CreateTaskDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            title, description = dialog.get_result()
            if title:
                self.create_requested.emit(title, description or "")
           

    def set_tasks(self, tasks: list[TaskEntity]) -> None:
        """Set the tasks to display.

        Args:
            tasks: List of TaskEntity objects to display.
        """
        self._clear_task_widgets()

        for task in tasks:
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

            self._scroll_layout.insertWidget(
                self._scroll_layout.count() - 1,
                task_widget
            )
            self._task_widgets[task.id] = task_widget  # type: ignore

    def _clear_task_widgets(self) -> None:
        """Remove all task widgets from the layout."""
        for i in range(self._scroll_layout.count() - 1):
            item = self._scroll_layout.itemAt(i)
            if item and item.widget():
                item.widget().deleteLater()
        self._task_widgets.clear()

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
                widget.deleteLater()
        elif operation == 'delete':
            if result.success and task_id in self._task_widgets:
                widget = self._task_widgets.pop(task_id)
                widget.deleteLater()

    def add_task(self, task: TaskEntity) -> None:
        """Add a single task to the view.

        Args:
            task: TaskEntity to add.
        """
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

        self._scroll_layout.insertWidget(
            self._scroll_layout.count() - 1,
            task_widget
        )
        self._task_widgets[task.id] = task_widget  # type: ignore
