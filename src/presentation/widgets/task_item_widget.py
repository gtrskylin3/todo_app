"""Custom widget for displaying a single task item.

This module provides the TaskItemWidget which displays a task in a
Markdown checkbox style with expandable details section.
"""

from datetime import datetime

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
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
                 parent: QWidget | None = None):
        """Initialize the task item widget.
        
        Args:
            task_id: Unique identifier for the task.
            title: Task title.
            description: Task description (optional).
            created_at: Task creation timestamp.
            completed_at: Task completion timestamp (None if not completed).
            parent: Parent widget.
        """
        super().__init__(parent)

        self._task_id = task_id
        self._title = title
        self._description = description
        self._created_at = created_at
        self._completed_at = completed_at
        self._is_expanded = False

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(4)

        # Top row: checkbox, title, date
        top_layout = QHBoxLayout()
        top_layout.setSpacing(8)

        # Checkbox
        self._checkbox = QCheckBox()
        self._checkbox.setChecked(self._completed_at is not None)
        self._checkbox.stateChanged.connect(self._on_checkbox_changed)
        top_layout.addWidget(self._checkbox)

        # Title label (clickable)
        self._title_label = QLabel(self._title)
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
        self._date_label = QLabel(f"[{date_str}]")
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
            reopen_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            reopen_btn.clicked.connect(self._on_reopen_clicked)
            reopen_btn.setFixedWidth(80)
            button_layout.addWidget(reopen_btn)
        else:
            # Edit button
            edit_btn = QPushButton("Edit")
            edit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            edit_btn.clicked.connect(self._on_edit_clicked)
            edit_btn.setFixedWidth(60)
            button_layout.addWidget(edit_btn)

            # Delete button
            delete_btn = QPushButton("Remove")
            delete_btn.setCursor(Qt.CursorShape.PointingHandCursor)
            delete_btn.clicked.connect(self._on_delete_clicked)
            delete_btn.setFixedWidth(70)
            button_layout.addWidget(delete_btn)

        button_layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        ))
        expanded_layout.addLayout(button_layout)

        self._expanded_widget.setVisible(False)
        main_layout.addWidget(self._expanded_widget)

    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets for modern appearance."""
        self.setStyleSheet("""
            TaskItemWidget {
                background-color: #2b2b2b;
                border-radius: 6px;
                border: 1px solid #3e3e3e;
            }
            TaskItemWidget:hover {
                border: 1px solid #505050;
            }
            QCheckBox {
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #505050;
                background-color: #3e3e3e;
            }
            QCheckBox::indicator:checked {
                background-color: #4a9eff;
                border: 2px solid #4a9eff;
            }
            QCheckBox::indicator:hover {
                border: 2px solid #6aafff;
            }
            QLabel {
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #3e3e3e;
                border: 1px solid #505050;
                border-radius: 4px;
                padding: 6px 12px;
                color: #e0e0e0;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border: 1px solid #6a6a6a;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
            QPushButton#deleteButton {
                background-color: #5a2a2a;
                border: 1px solid #7a3a3a;
            }
            QPushButton#deleteButton:hover {
                background-color: #6a3a3a;
            }
        """)

    def _get_date_string(self) -> str:
        """Get the date string for display.
        
        Returns:
            str: Formatted date string (DD/MM).
        """
        if self._completed_at:
            return self._completed_at.strftime("%d/%m")
        return self._created_at.strftime("%d/%m")

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
        self._checkbox.blockSignals(True)
        self._checkbox.setChecked(is_completed)
        self._checkbox.blockSignals(False)
