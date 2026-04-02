"""View for displaying completed tasks grouped by date.

This module provides the CompletedTasksView which shows completed tasks
organized by their completion date in reverse chronological order.
"""

from datetime import datetime

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QLabel, QScrollArea, QVBoxLayout, QWidget

from src.domain.task_entity import TaskEntity
from src.presentation.styles import get_completed_tasks_view_styles
from src.presentation.widgets.date_group_widget import DateGroupWidget
from src.presentation.widgets.task_item_widget import TaskItemWidget


class CompletedTasksView(QWidget):
    """View for displaying completed tasks grouped by date.
    
    This view shows completed tasks organized by their completion date,
    with dates in reverse chronological order. Each date group can be
    expanded/collapsed to show/hide tasks.
    
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
        self._groups_layout.setSpacing(8)
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
        """Clear all date groups and task widgets."""
        for group in self._date_groups.values():
            group.deleteLater()
        for widget in self._task_widgets.values():
            widget.deleteLater()
        self._date_groups.clear()
        self._task_widgets.clear()

    def _get_or_create_date_group(self, date_value: datetime) -> DateGroupWidget:
        """Get or create a date group widget.
        
        Args:
            date_value: Date for the group.
            
        Returns:
            DateGroupWidget: The date group widget.
        """
        if date_value not in self._date_groups:
            group = DateGroupWidget(date_value)

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

            # Hide empty state
            if self._empty_label:
                self._empty_label.setVisible(False)

        return self._date_groups[date_value]

    def add_task(self, task: TaskEntity) -> None:
        """Add a completed task to the appropriate date group.
        
        Args:
            task: Completed task entity to display.
        """
        if not task.completed_at:
            return

        # Get the date (without time)
        completion_date = task.completed_at

        # Get or create date group
        group = self._get_or_create_date_group(completion_date)

        # Create task widget (hide checkbox for completed view)
        task_widget = TaskItemWidget(
            task_id=task.id,  # type: ignore
            title=task.title,
            description=task.description,
            created_at=task.created_at,
            completed_at=task.completed_at,
            show_checkbox=False
        )

        # Connect signals
        task_widget.reopen_requested.connect(self.reopen_requested.emit)

        # Add to group
        group.add_task_widget(task_widget)
        self._task_widgets[task.id] = task_widget  # type: ignore

        # Update count and expand
        count = len([w for w in self._task_widgets.values()
                     if w._completed_at and
                     w._completed_at.date() == completion_date.date()])
        group.set_task_count(count)
        group.set_expanded(True)

    def remove_task(self, task_id: int) -> None:
        """Remove a task from the view.
        
        Args:
            task_id: ID of the task to remove.
        """
        if task_id in self._task_widgets:
            widget = self._task_widgets.pop(task_id)

            # Find and remove from date group
            for _group in self._date_groups.values():
                # We need to find which group contains this widget
                # by checking the layout
                pass

            widget.deleteLater()

            # TODO: Update group counts and remove empty groups

    def set_tasks_by_date(self, tasks_by_date: dict[datetime, list[TaskEntity]]) -> None:
        """Set tasks organized by completion date.
        
        Args:
            tasks_by_date: Dictionary mapping dates to lists of tasks.
        """
        self.clear_all()

        # Sort dates in reverse chronological order
        sorted_dates = sorted(tasks_by_date.keys(), reverse=True)

        for date_value in sorted_dates:
            tasks = tasks_by_date[date_value]
            if tasks:
                group = self._get_or_create_date_group(date_value)

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
                group.set_expanded(True)

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
                    break
        
        # Remove widget
        task_widget.deleteLater()

        # Show empty state if no tasks
        if not self._task_widgets and self._empty_label:
            self._empty_label.setVisible(True)
