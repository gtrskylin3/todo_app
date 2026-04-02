"""View for displaying completed tasks grouped by month and date.

This module provides the CompletedTasksView which shows completed tasks
organized by month, then by date within each month.
"""

from datetime import datetime
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget, QHBoxLayout

from src.domain.task_entity import TaskEntity
from src.presentation.styles import get_completed_tasks_view_styles
from src.presentation.widgets.date_group_widget import DateGroupWidget
from src.presentation.widgets.task_item_widget import TaskItemWidget


class CompletedTasksView(QWidget):
    """View for displaying completed tasks grouped by month and date.

    This view shows completed tasks organized by month (collapsed by default),
    with dates within each month also collapsed by default.
    Users can expand months and dates as needed.

    Signals:
        reopen_requested: Emitted when a task should be reopened (task_id: int).
    """

    reopen_requested = pyqtSignal(int)

    def __init__(self, parent: QWidget | None = None):
        """Initialize the completed tasks view.

        Args:
            parent: Parent widget.
        """
        super().__init__(parent)
        self.setObjectName("completedTasksView")

        self._date_groups: dict[datetime, DateGroupWidget] = {}
        self._month_groups: dict[str, QWidget] = {}
        self._month_layouts: dict[str, QVBoxLayout] = {}
        self._month_expanded: dict[str, bool] = {}
        self._task_widgets: dict[int, TaskItemWidget] = {}

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Header
        header_label = QLabel("Completed Tasks")
        header_label.setObjectName("headerLabel")
        header_font = QFont()
        header_font.setPointSize(18)
        header_font.setWeight(QFont.Weight.Bold)
        header_label.setFont(header_font)
        layout.addWidget(header_label)

        # Scroll area for date groups
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Container for date groups
        self._groups_container = QWidget()
        self._groups_layout = QVBoxLayout(self._groups_container)
        self._groups_layout.setContentsMargins(0, 0, 0, 0)
        self._groups_layout.setSpacing(12)
        self._groups_layout.addStretch()

        self._scroll_area.setWidget(self._groups_container)
        layout.addWidget(self._scroll_area)

        # Empty state label
        self._empty_label = QLabel("No completed tasks yet.")
        empty_font = QFont()
        empty_font.setPointSize(11)
        self._empty_label.setFont(empty_font)
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._groups_layout.addWidget(self._empty_label)

    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets for modern appearance."""
        self.setStyleSheet(get_completed_tasks_view_styles())

    def clear_all(self) -> None:
        """Clear all date groups, month groups, and task widgets."""
        for group in self._date_groups.values():
            group.deleteLater()
        for month_widget in self._month_groups.values():
            month_widget.deleteLater()
        for widget in self._task_widgets.values():
            widget.deleteLater()
        self._date_groups.clear()
        self._month_groups.clear()
        self._month_layouts.clear()
        self._month_expanded.clear()
        self._task_widgets.clear()

    def _get_month_key(self, date_value: datetime) -> str:
        """Get month key for a date.

        Args:
            date_value: The date to get month key for.

        Returns:
            str: Month key in format "Month Year" (e.g., "March 2026").
        """
        month_names = {
            1: "January", 2: "February", 3: "March", 4: "April",
            5: "May", 6: "June", 7: "July", 8: "August",
            9: "September", 10: "October", 11: "November", 12: "December"
        }
        return f"{month_names[date_value.month]} {date_value.year}"

    def _get_month_sort_key(self, month_key: str) -> tuple:
        """Get sort key for month (year, month) for proper sorting.

        Args:
            month_key: Month key in format "Month Year".

        Returns:
            tuple: (year, month) tuple for sorting.
        """
        parts = month_key.split()
        month_name = parts[0]
        year = int(parts[1])
        month_map = {
            "January": 1, "February": 2, "March": 3, "April": 4,
            "May": 5, "June": 6, "July": 7, "August": 8,
            "September": 9, "October": 10, "November": 11, "December": 12
        }
        return (year, month_map[month_name])

    def _toggle_month(self, month_key: str) -> None:
        """Toggle month expanded/collapsed state.

        Args:
            month_key: Month key to toggle.
        """
        if month_key not in self._month_groups:
            return

        # Find the date container
        month_widget = self._month_groups[month_key]
        date_container = None
        for i in range(month_widget.layout().count()):
            item = month_widget.layout().itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QWidget):
                widget = item.widget()
                if widget != month_widget:  # Not the header itself
                    date_container = widget
                    break

        if date_container:
            self._month_expanded[month_key] = not self._month_expanded.get(month_key, False)
            date_container.setVisible(self._month_expanded[month_key])

    def _get_or_create_month_group(self, date_value: datetime) -> QWidget:
        """Get or create a month group widget.

        Args:
            date_value: Date for the month group.

        Returns:
            QWidget: The month group widget with header.
        """
        month_key = self._get_month_key(date_value)

        if month_key not in self._month_groups:
            # Create month container
            month_widget = QWidget()
            month_widget.setObjectName("monthGroup")
            month_layout = QVBoxLayout(month_widget)
            month_layout.setContentsMargins(0, 0, 0, 0)
            month_layout.setSpacing(4)

            # Month header with expand/collapse
            header_layout = QHBoxLayout()
            header_layout.setContentsMargins(0, 0, 0, 0)
            header_layout.setSpacing(8)

            # Expand/collapse indicator
            indicator = QLabel("▶")
            indicator.setObjectName("monthIndicator")
            indicator.setFixedWidth(16)
            header_layout.addWidget(indicator)

            # Month header label
            month_header = QLabel(month_key)
            month_header.setObjectName("monthHeaderLabel")
            month_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
            month_header.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            header_layout.addWidget(month_header)
            header_layout.addStretch()

            month_layout.addLayout(header_layout)

            # Container for date groups within this month
            date_container = QWidget()
            date_layout = QVBoxLayout(date_container)
            date_layout.setContentsMargins(24, 4, 0, 0)  # Indent date groups
            date_layout.setSpacing(4)
            date_container.setVisible(False)  # Collapsed by default
            month_layout.addWidget(date_container)

            # Store expanded state
            self._month_expanded[month_key] = False

            # Connect click handler
            def make_toggle_handler(key=month_key):
                def handler():
                    self._toggle_month(key)
                    # Update indicator
                    widget = self._month_groups.get(key)
                    if widget:
                        indicator_label = widget.findChild(QLabel, "monthIndicator")
                        if indicator_label:
                            indicator_label.setText("▼" if self._month_expanded.get(key, False) else "▶")
                return handler

            month_header.mousePressEvent = lambda e, h=make_toggle_handler(): h()
            indicator.mousePressEvent = lambda e, h=make_toggle_handler(): h()

            # Insert in chronological order (newest first)
            month_keys = sorted(self._month_groups.keys(), 
                               key=self._get_month_sort_key, 
                               reverse=True)
            insert_index = 0
            for i, key in enumerate(month_keys):
                if self._get_month_sort_key(month_key) > self._get_month_sort_key(key):
                    insert_index = i
                    break
                insert_index = i + 1

            # Insert before the stretch
            stretch_item = self._groups_layout.takeAt(self._groups_layout.count() - 1)
            self._groups_layout.insertWidget(insert_index, month_widget)
            if stretch_item:
                self._groups_layout.addItem(stretch_item)

            self._month_groups[month_key] = month_widget
            self._month_layouts[month_key] = date_layout

        return self._month_groups[month_key]

    def _get_or_create_date_group(self, date_value: datetime) -> DateGroupWidget:
        """Get or create a date group widget within its month.

        Args:
            date_value: Date for the group.

        Returns:
            DateGroupWidget: The date group widget.
        """
        if date_value not in self._date_groups:
            group = DateGroupWidget(date_value)
            group.set_expanded(False)  # Collapsed by default

            # Get month group
            month_key = self._get_month_key(date_value)
            month_widget = self._get_or_create_month_group(date_value)
            date_layout = self._month_layouts[month_key]

            # Insert in chronological order (newest first) within month
            dates_in_month = [d for d in self._date_groups.keys() 
                             if self._get_month_key(d) == month_key]
            dates_in_month.sort(reverse=True)

            insert_index = 0
            for i, d in enumerate(dates_in_month):
                if date_value > d:
                    insert_index = i
                    break
                insert_index = i + 1

            date_layout.insertWidget(insert_index, group)
            self._date_groups[date_value] = group

        return self._date_groups[date_value]

    def set_tasks_by_date(self, tasks_by_date: dict[datetime, list[TaskEntity]]) -> None:
        """Set tasks organized by completion date, grouped by month.

        Args:
            tasks_by_date: Dictionary mapping dates to lists of tasks.
        """
        self.clear_all()

        if not tasks_by_date:
            return

        # Sort dates in reverse chronological order
        sorted_dates = sorted(tasks_by_date.keys(), reverse=True)

        for date_value in sorted_dates:
            tasks = tasks_by_date[date_value]
            if tasks:
                group = self._get_or_create_date_group(date_value)
                group.set_expanded(False)  # Collapsed by default

                for task in tasks:
                    task_widget = TaskItemWidget(
                        task_id=task.id,  # type: ignore
                        title=task.title,
                        description=task.description,
                        created_at=task.created_at,
                        completed_at=task.completed_at,
                        show_checkbox=False
                    )

                    task_widget.reopen_requested.connect(self.reopen_requested.emit)

                    group.add_task_widget(task_widget)
                    self._task_widgets[task.id] = task_widget  # type: ignore

                group.set_task_count(len(tasks))

        # Hide empty state if we have tasks
        if self._task_widgets and self._empty_label:
            self._empty_label.setVisible(False)

    def handle_reopen(self, task_id: int) -> None:
        """Handle reopening a task (remove from completed view).

        Args:
            task_id: ID of the task being reopened.
        """
        if task_id not in self._task_widgets:
            return

        # Get the task widget to find its completion date
        task_widget = self._task_widgets[task_id]
        completed_at = task_widget._completed_at

        # Remove from task widgets dict
        del self._task_widgets[task_id]

        # Find and update the date group
        if completed_at:
            completion_date = completed_at.date()
            for date_value, group in self._date_groups.items():
                if date_value.date() == completion_date:
                    group.remove_task_widget(task_id)

                    # Remove empty group
                    if group._content_layout.count() == 0:
                        group.deleteLater()
                        del self._date_groups[date_value]

                        # Check if month is now empty
                        month_key = self._get_month_key(date_value)
                        month_dates = [d for d in self._date_groups.keys()
                                      if self._get_month_key(d) == month_key]
                        if not month_dates:
                            month_widget = self._month_groups.pop(month_key, None)
                            if month_widget:
                                month_widget.deleteLater()
                            self._month_layouts.pop(month_key, None)
                            self._month_expanded.pop(month_key, None)
                    break

        # Remove widget
        task_widget.deleteLater()

        # Show empty state if no tasks
        if not self._task_widgets and self._empty_label:
            self._empty_label.setVisible(True)
