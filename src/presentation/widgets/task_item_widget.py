"""Custom widget for displaying a single task item.

This module provides the TaskItemWidget which displays a task in a
Markdown checkbox style with expandable details section.
"""

from datetime import datetime

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class TaskItemWidget(QFrame):
    """Custom widget for displaying a task with Markdown-style checkbox.
    
    This widget displays a task in the format: [ ] Task Title [DD/MM]
    Clicking the checkbox toggles completion. Clicking the title expands
    an accordion section with details and action buttons.
    
    Signals:
        checked: Emitted when the checkbox is toggled (task_id: int).
        edit_requested: Emitted when edit button is clicked (task_id: int).
        delete_requested: Emitted when delete button is clicked (task_id: int).
        reopen_requested: Emitted when reopen button is clicked (task_id: int).
    """

    checked = pyqtSignal(int)
    edit_requested = pyqtSignal(int)
    delete_requested = pyqtSignal(int)
    reopen_requested = pyqtSignal(int)

    def __init__(self, task_id: int, title: str, description: str | None,
                 created_at: datetime, completed_at: datetime | None,
                 show_checkbox: bool = True,
                 parent: QWidget | None = None):
        """Initialize the task item widget.

        Args:
            task_id: Unique identifier for the task.
            title: Task title.
            description: Task description (optional).
            created_at: Task creation timestamp.
            completed_at: Task completion timestamp (None if not completed).
            show_checkbox: Whether to show the checkbox (True for active tasks).
            parent: Parent widget.
        """
        super().__init__(parent)

        self._task_id = task_id
        self._title = title
        self._description = description
        self._created_at = created_at
        self._completed_at = completed_at
        self._show_checkbox = show_checkbox
        self._is_expanded = False

        # Set object name for styling
        self.setObjectName("taskCard")

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(4)

        # Top row: checkbox (optional), title, date
        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)

        # Checkbox (only for active tasks)
        if self._show_checkbox:
            self._checkbox = QCheckBox()
            self._checkbox.setChecked(self._completed_at is not None)
            self._checkbox.stateChanged.connect(self._on_checkbox_changed)
            top_layout.addWidget(self._checkbox)
        else:
            self._checkbox = None

        # Title label (clickable)
        self._title_label = QLabel(self._title)
        self._title_label.setObjectName("titleLabel")
        self._title_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self._title_label.mousePressEvent = self._on_title_clicked  # type: ignore
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setWeight(QFont.Weight.Bold)
        self._title_label.setFont(title_font)
        self._title_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        top_layout.addWidget(self._title_label, 1)

        # Date label
        date_str = self._get_date_string()
        self._date_label = QLabel(date_str)
        self._date_label.setObjectName("dateLabel")
        date_font = QFont()
        date_font.setPointSize(9)
        self._date_label.setFont(date_font)
        top_layout.addWidget(self._date_label)

        main_layout.addLayout(top_layout)

        # Expanded section (details and buttons)
        self._expanded_widget = QWidget()
        expanded_layout = QVBoxLayout(self._expanded_widget)
        expanded_layout.setContentsMargins(28, 8, 8, 8)
        expanded_layout.setSpacing(8)

        # Description
        if self._description:
            desc_label = QLabel(self._description)
            desc_label.setWordWrap(True)
            desc_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            desc_font = QFont()
            desc_font.setPointSize(10)
            desc_label.setFont(desc_font)
            expanded_layout.addWidget(desc_label)

        # Created at label
        created_str = self._created_at.strftime("%d/%m/%Y %H:%M")
        created_label = QLabel(f"Created: {created_str}")
        created_font = QFont()
        created_font.setPointSize(9)
        created_label.setFont(created_font)
        expanded_layout.addWidget(created_label)

        # Action buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        if self._completed_at is not None:
            # Reopen button for completed tasks
            reopen_btn = QPushButton("Reopen")
            reopen_btn.setObjectName("reopenButton")
            reopen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            reopen_btn.clicked.connect(self._on_reopen_clicked)
            reopen_btn.setMinimumWidth(100)
            button_layout.addWidget(reopen_btn)
        else:
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("editButton")
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.clicked.connect(self._on_edit_clicked)
            edit_btn.setMinimumWidth(80)
            button_layout.addWidget(edit_btn)

            # Delete button
            delete_btn = QPushButton("🗑 Remove")
            delete_btn.setObjectName("deleteButton")
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_btn.clicked.connect(self._on_delete_clicked)
            delete_btn.setMinimumWidth(100)
            button_layout.addWidget(delete_btn)

        button_layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        ))
        expanded_layout.addLayout(button_layout)

        self._expanded_widget.setVisible(False)
        main_layout.addWidget(self._expanded_widget)

    def _get_date_string(self) -> str:
        """Get the date string for display.

        Returns:
            str: Formatted date string (e.g., "30 марта").
        """
        # Русские названия месяцев
        month_names = {
            1: "января", 2: "февраля", 3: "марта", 4: "апреля",
            5: "мая", 6: "июня", 7: "июля", 8: "августа",
            9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"
        }
        
        if self._completed_at:
            date = self._completed_at
        else:
            date = self._created_at
            
        day = date.day
        month = month_names.get(date.month, "")
        
        return f"{day} {month}"

    def _on_checkbox_changed(self, state: int) -> None:
        """Handle checkbox state change.
        
        Args:
            state: Checkbox state (0 for unchecked, 2 for checked).
        """
        self.checked.emit(self._task_id)

    def _on_title_clicked(self, event) -> None:
        """Handle title label click to toggle expansion.
        
        Args:
            event: Mouse event.
        """
        self._is_expanded = not self._is_expanded
        self._expanded_widget.setVisible(self._is_expanded)

    def _on_edit_clicked(self) -> None:
        """Handle edit button click."""
        self.edit_requested.emit(self._task_id)

    def _on_delete_clicked(self) -> None:
        """Handle delete button click."""
        self.delete_requested.emit(self._task_id)

    def _on_reopen_clicked(self) -> None:
        """Handle reopen button click."""
        self.reopen_requested.emit(self._task_id)

    def get_task_id(self) -> int:
        """Get the task ID.
        
        Returns:
            int: Task ID.
        """
        return self._task_id

    def update_completion_status(self, is_completed: bool) -> None:
        """Update the checkbox state without emitting signal.

        Args:
            is_completed: Whether the task is completed.
        """
        if self._checkbox:
            self._checkbox.blockSignals(True)
            self._checkbox.setChecked(is_completed)
            self._checkbox.blockSignals(False)

    def hide_checkbox(self) -> None:
        """Hide the checkbox for completed tasks view.
        
        Note: This method is kept for backward compatibility.
        Use show_checkbox=False in constructor instead.
        """
        if self._checkbox:
            self._checkbox.setVisible(False)
