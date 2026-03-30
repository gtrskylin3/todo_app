"""Custom widget for grouping completed tasks by date.

This module provides the DateGroupWidget which displays a collapsible
date header with a list of tasks completed on that date.
"""

from datetime import datetime

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)


class DateGroupWidget(QFrame):
    """Custom widget for grouping tasks by completion date.
    
    This widget displays a date header that can be clicked to expand/collapse
    a list of tasks completed on that date.
    
    Signals:
        expanded: Emitted when the widget is expanded.
        collapsed: Emitted when the widget is collapsed.
    """

    expanded = pyqtSignal()
    collapsed = pyqtSignal()

    def __init__(self, date_value: datetime, parent: QWidget | None = None):
        """Initialize the date group widget.

        Args:
            date_value: The date for this group.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setObjectName("dateGroupWidget")

        self._date_value = date_value
        self._is_expanded = False

        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Header
        header_widget = QWidget()
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(12, 10, 12, 10)

        # Expand/collapse indicator
        self._indicator_label = QLabel("▶")
        self._indicator_label.setObjectName("indicatorLabel")
        indicator_font = QFont()
        indicator_font.setPointSize(10)
        self._indicator_label.setFont(indicator_font)
        self._indicator_label.setFixedWidth(20)
        header_layout.addWidget(self._indicator_label)

        # Date label
        date_str = self._date_value.strftime("%d %B %Y")
        self._date_label = QLabel(date_str)
        self._date_label.setObjectName("dateHeaderTitle")
        date_font = QFont()
        date_font.setPointSize(12)
        date_font.setWeight(QFont.Weight.Bold)
        self._date_label.setFont(date_font)
        header_layout.addWidget(self._date_label)

        header_layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        ))

        # Task count label
        self._count_label = QLabel("(0 tasks)")
        self._count_label.setObjectName("dateHeaderCount")
        count_font = QFont()
        count_font.setPointSize(10)
        self._count_label.setFont(count_font)
        header_layout.addWidget(self._count_label)

        # Make header clickable
        header_widget.setCursor(Qt.CursorShape.PointingHandCursor)
        header_widget.mousePressEvent = self._on_header_clicked  # type: ignore

        main_layout.addWidget(header_widget)

        # Content area (for task widgets)
        self._content_widget = QWidget()
        self._content_layout = QVBoxLayout(self._content_widget)
        self._content_layout.setContentsMargins(12, 0, 12, 10)
        self._content_layout.setSpacing(4)

        self._content_widget.setVisible(False)
        main_layout.addWidget(self._content_widget)

    def _on_header_clicked(self, event) -> None:
        """Handle header click to toggle expansion.
        
        Args:
            event: Mouse event.
        """
        self._is_expanded = not self._is_expanded
        self._content_widget.setVisible(self._is_expanded)

        # Update indicator
        if self._is_expanded:
            self._indicator_label.setText("▼")
            self.expanded.emit()
        else:
            self._indicator_label.setText("▶")
            self.collapsed.emit()

    def add_task_widget(self, widget: QWidget) -> None:
        """Add a task widget to the content area.
        
        Args:
            widget: Task widget to add.
        """
        self._content_layout.addWidget(widget)

    def clear_tasks(self) -> None:
        """Remove all task widgets from the content area."""
        while self._content_layout.count():
            item = self._content_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def remove_task_widget(self, task_id: int) -> None:
        """Remove a specific task widget by ID.

        Args:
            task_id: ID of the task to remove.
        """
        for i in range(self._content_layout.count()):
            item = self._content_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if hasattr(widget, '_task_id') and widget._task_id == task_id:
                    widget.deleteLater()
                    self._content_layout.removeWidget(widget)
                    # Update count
                    new_count = self._content_layout.count()
                    self.set_task_count(new_count)
                    break

    def set_task_count(self, count: int) -> None:
        """Set the task count display.
        
        Args:
            count: Number of tasks.
        """
        task_word = "task" if count == 1 else "tasks"
        self._count_label.setText(f"({count} {task_word})")

    def is_expanded(self) -> bool:
        """Check if the widget is expanded.
        
        Returns:
            bool: True if expanded, False otherwise.
        """
        return self._is_expanded

    def set_expanded(self, expanded: bool) -> None:
        """Set the expansion state.
        
        Args:
            expanded: True to expand, False to collapse.
        """
        if expanded != self._is_expanded:
            self._is_expanded = expanded
            self._content_widget.setVisible(expanded)

            if expanded:
                self._indicator_label.setText("▼")
            else:
                self._indicator_label.setText("▶")

    def get_date(self) -> datetime:
        """Get the date for this group.
        
        Returns:
            datetime: The grouped date.
        """
        return self._date_value
