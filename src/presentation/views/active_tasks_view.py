"""View for displaying active (non-completed) tasks.

This module provides the ActiveTasksView which shows all non-completed
tasks with a quick-add input field at the top.
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from src.application.task_service import TaskServiceResult
from src.domain.task_entity import TaskEntity
from src.presentation.styles import get_global_styles
from src.presentation.widgets.task_item_widget import TaskItemWidget


class ActiveTasksView(QWidget):
    """View for displaying and managing active tasks.
    
    This view shows all non-completed tasks in a scrollable area
    with a quick-add input field at the top.
    
    Signals:
        create_requested: Emitted when a new task should be created (title: str).
        toggle_requested: Emitted when task completion should be toggled (task_id: int).
        edit_requested: Emitted when task edit is requested (task_id: int).
        delete_requested: Emitted when task deletion is requested (task_id: int).
    """

    create_requested = pyqtSignal(str)
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

        # Quick add input
        add_layout = QHBoxLayout()
        add_layout.setSpacing(8)

        self._add_input = QLineEdit()
        self._add_input.setPlaceholderText("Add a new task... Press Enter to create")
        self._add_input.setFixedHeight(40)
        self._add_input.returnPressed.connect(self._on_add_pressed)
        self._add_input.setStyleSheet("""
            QLineEdit {
                background-color: #1A1A1A;
                border: 1px solid #6B6B6B;
                border-radius: 8px;
                padding: 12px 16px;
                color: #FFFFFF;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 2px solid #8B5CF6;
                background-color: #1A1A1A;
            }
            QLineEdit::placeholder {
                color: #A0A0A0;
            }
        """)
        add_layout.addWidget(self._add_input, 1)

        add_btn = QPushButton("Add")
        add_btn.setObjectName("addButton")
        add_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        add_btn.setFixedHeight(40)
        add_btn.setFixedWidth(80)
        add_btn.clicked.connect(self._on_add_clicked)
        add_btn.setStyleSheet("""
            QPushButton#addButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8B5CF6, stop:1 #7C3AED);
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                color: #FFFFFF;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton#addButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9B6CF6, stop:1 #8C4AED);
            }
            QPushButton#addButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7C3AED, stop:1 #6D28D9);
            }
        """)
        add_layout.addWidget(add_btn)

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
        self._scroll_area.setFixedHeight(400)
        layout.addWidget(self._scroll_area)

        # Empty state label
        self._empty_label = QLabel("No active tasks. Add one above!")
        self._empty_label.setObjectName("emptyStateLabel")
        self._empty_label.setStyleSheet("""
            QLabel#emptyStateLabel {
                color: #A0A0A0;
                font-size: 13px;
                background-color: transparent;
            }
        """)
        empty_font = QFont()
        empty_font.setPointSize(11)
        self._empty_label.setFont(empty_font)
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._tasks_layout.addWidget(self._empty_label)

    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets for modern appearance."""
        self.setStyleSheet(get_global_styles())

    def _on_add_pressed(self) -> None:
        """Handle Enter key press in add input."""
        self._try_add_task()

    def _on_add_clicked(self) -> None:
        """Handle add button click."""
        self._try_add_task()

    def _try_add_task(self) -> None:
        """Try to create a new task from the input."""
        title = self._add_input.text().strip()
        if title:
            self.create_requested.emit(title)
            self._add_input.clear()

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
