"""Main window for the TODO application.

This module provides the MainWindow class which integrates all views
and handles the application logic with background threading.
"""

import logging

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QCloseEvent
from PyQt6.QtWidgets import (
    QMainWindow,
    QMessageBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.application.task_service import TaskService, TaskServiceResult
from src.config.settings import AppConfig
from src.presentation.views.active_tasks_view import ActiveTasksView
from src.presentation.views.completed_tasks_view import CompletedTasksView
from src.presentation.widgets.edit_task_dialog import EditTaskDialog
from src.presentation.workers.db_worker import DatabaseWorker

logger = logging.getLogger(__name__)


class MainWindow(QMainWindow):
    """Main application window.
    
    This window contains tabs for active and completed tasks views,
    and orchestrates all user interactions with background database operations.
    
    Args:
        task_service: TaskService instance for business logic.
        config: Application configuration.
    """

    def __init__(self, task_service: TaskService, config: AppConfig):
        """Initialize the main window.

        Args:
            task_service: TaskService for business operations.
            config: Application configuration.
        """
        super().__init__()

        self._task_service = task_service
        self._config = config
        self._workers: list[DatabaseWorker] = []  # Track all workers

        self._setup_ui()
        self._apply_styles()
        self._load_initial_data()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        self.setWindowTitle(self._config.app_name)
        self.setMinimumSize(600, 700)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Tab widget
        self._tab_widget = QTabWidget()
        self._tab_widget.setDocumentMode(True)

        # Active tasks view
        self._active_view = ActiveTasksView()
        self._active_view.create_requested.connect(self._on_create_task)
        self._active_view.toggle_requested.connect(self._on_toggle_task)
        self._active_view.edit_requested.connect(self._on_edit_task)
        self._active_view.delete_requested.connect(self._on_delete_task)
        self._active_view.reopen_requested.connect(self._on_reopen_task)

        # Completed tasks view
        self._completed_view = CompletedTasksView()
        self._completed_view.reopen_requested.connect(self._on_reopen_task)

        self._tab_widget.addTab(self._active_view, "Active")
        self._tab_widget.addTab(self._completed_view, "Completed")

        layout.addWidget(self._tab_widget)

    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets for modern dark theme."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QTabWidget::pane {
                border: none;
                background-color: #1e1e1e;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #a0a0a0;
                padding: 12px 24px;
                border: none;
                border-bottom: 2px solid transparent;
                font-size: 13px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border-bottom: 2px solid #4a9eff;
            }
            QTabBar::tab:hover:!selected {
                background-color: #353535;
                color: #c0c0c0;
            }
        """)

    def _load_initial_data(self) -> None:
        """Load initial task data from the database."""
        self._load_active_tasks()
        self._load_completed_tasks()

    def _load_active_tasks(self) -> None:
        """Load active tasks in a background thread."""
        def fetch_active():
            return self._task_service.get_all_active_tasks()

        worker = DatabaseWorker(fetch_active)
        worker.signals.result.connect(self._on_active_tasks_loaded)
        worker.signals.error.connect(self._on_operation_error)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()

    def _load_completed_tasks(self) -> None:
        """Load completed tasks in a background thread."""
        def fetch_completed():
            dates = self._task_service.get_all_completed_dates()
            tasks_by_date = {}
            for date_value in dates:
                tasks = self._task_service.get_completed_tasks_by_date(date_value)
                if tasks:
                    tasks_by_date[date_value] = tasks
            return tasks_by_date

        worker = DatabaseWorker(fetch_completed)
        worker.signals.result.connect(self._on_completed_tasks_loaded)
        worker.signals.error.connect(self._on_operation_error)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()
    
    def _cleanup_worker(self, worker: DatabaseWorker) -> None:
        """Remove a finished worker from the list.
        
        Args:
            worker: The finished worker to remove.
        """
        if worker in self._workers:
            self._workers.remove(worker)

    def _on_active_tasks_loaded(self, tasks) -> None:
        """Handle active tasks loaded from database.
        
        Args:
            tasks: List of TaskEntity objects.
        """
        self._active_view.set_tasks(tasks)
        logger.debug(f"Loaded {len(tasks)} active tasks")

    def _on_completed_tasks_loaded(self, tasks_by_date) -> None:
        """Handle completed tasks loaded from database.
        
        Args:
            tasks_by_date: Dictionary mapping dates to task lists.
        """
        self._completed_view.set_tasks_by_date(tasks_by_date)
        logger.debug(f"Loaded completed tasks for {len(tasks_by_date)} dates")

    def _on_create_task(self, title: str) -> None:
        """Handle create task request.

        Args:
            title: Task title.
        """
        def create():
            return self._task_service.create_task(title)

        worker = DatabaseWorker(create)
        worker.signals.result.connect(self._on_create_result)
        worker.signals.error.connect(self._on_operation_error)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()

    def _on_create_result(self, result: TaskServiceResult) -> None:
        """Handle create task result.
        
        Args:
            result: Result of the create operation.
        """
        if result.success:
            logger.info(f"Task created: {result.task.title if result.task else 'unknown'}")
            self._active_view.handle_operation_result(result, 'create')
            # Reload completed tasks in case we need to refresh
            self._load_completed_tasks()
        else:
            self._show_error_message(f"Failed to create task: {result.error}")

    def _on_toggle_task(self, task_id: int) -> None:
        """Handle toggle task completion request.

        Args:
            task_id: ID of the task to toggle.
        """
        def toggle():
            return self._task_service.toggle_task_completion(task_id)

        worker = DatabaseWorker(toggle)
        worker.signals.result.connect(lambda r: self._on_toggle_result(r, task_id))
        worker.signals.error.connect(self._on_operation_error)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()

    def _on_toggle_result(self, result: TaskServiceResult, task_id: int) -> None:
        """Handle toggle task result.
        
        Args:
            result: Result of the toggle operation.
            task_id: ID of the toggled task.
        """
        if result.success:
            self._active_view.handle_operation_result(result, 'toggle', task_id)
            # Reload completed tasks to show newly completed task
            self._load_completed_tasks()
        else:
            self._show_error_message(f"Failed to toggle task: {result.error}")

    def _on_edit_task(self, task_id: int) -> None:
        """Handle edit task request.
        
        Args:
            task_id: ID of the task to edit.
        """
        task = self._task_service.get_task(task_id)
        if not task:
            self._show_error_message("Task not found")
            return

        dialog = EditTaskDialog(task.title, task.description, self)
        if dialog.exec():
            new_title, new_description = dialog.get_result()
            self._update_task(task_id, new_title, new_description)

    def _update_task(self, task_id: int, title: str, description: str | None) -> None:
        """Update a task in the database.

        Args:
            task_id: ID of the task to update.
            title: New task title.
            description: New task description.
        """
        def update():
            return self._task_service.update_task(task_id, title, description)

        worker = DatabaseWorker(update)
        worker.signals.result.connect(self._on_update_result)
        worker.signals.error.connect(self._on_operation_error)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()

    def _on_update_result(self, result: TaskServiceResult) -> None:
        """Handle update task result.
        
        Args:
            result: Result of the update operation.
        """
        if result.success:
            logger.info(f"Task updated: {result.task.title if result.task else 'unknown'}")
            # Reload active tasks to show updated task
            self._load_active_tasks()
        else:
            self._show_error_message(f"Failed to update task: {result.error}")

    def _on_delete_task(self, task_id: int) -> None:
        """Handle delete task request.
        
        Args:
            task_id: ID of the task to delete.
        """
        # Show confirmation dialog
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            "Are you sure you want to delete this task?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            def delete():
                return self._task_service.delete_task(task_id)

            worker = DatabaseWorker(delete)
            worker.signals.result.connect(lambda r: self._on_delete_result(r, task_id))
            worker.signals.error.connect(self._on_operation_error)
            worker.finished.connect(lambda: self._cleanup_worker(worker))
            self._workers.append(worker)
            worker.start()

    def _on_delete_result(self, result: TaskServiceResult, task_id: int) -> None:
        """Handle delete task result.
        
        Args:
            result: Result of the delete operation.
            task_id: ID of the deleted task.
        """
        if result.success:
            logger.info(f"Task {task_id} deleted")
            self._active_view.handle_operation_result(result, 'delete', task_id)
        else:
            self._show_error_message(f"Failed to delete task: {result.error}")

    def _on_reopen_task(self, task_id: int) -> None:
        """Handle reopen task request.

        Args:
            task_id: ID of the task to reopen.
        """
        def reopen():
            return self._task_service.reopen_task(task_id)

        worker = DatabaseWorker(reopen)
        worker.signals.result.connect(lambda r: self._on_reopen_result(r, task_id))
        worker.signals.error.connect(self._on_operation_error)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()

    def _on_reopen_result(self, result: TaskServiceResult, task_id: int) -> None:
        """Handle reopen task result.
        
        Args:
            result: Result of the reopen operation.
            task_id: ID of the reopened task.
        """
        if result.success:
            logger.info(f"Task {task_id} reopened")
            self._completed_view.handle_reopen(task_id)
            # Reload active tasks to show reopened task
            self._load_active_tasks()
        else:
            self._show_error_message(f"Failed to reopen task: {result.error}")

    def _on_operation_error(self, error_message: str) -> None:
        """Handle database operation error.
        
        Args:
            error_message: Error message from the operation.
        """
        logger.error(f"Database operation error: {error_message}")
        self._show_error_message(f"Database error: {error_message}")

    def _show_error_message(self, message: str) -> None:
        """Show an error message to the user.

        Args:
            message: Error message to display.
        """
        QMessageBox.critical(
            self,
            "Error",
            message,
            QMessageBox.StandardButton.Ok
        )

    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close event to clean up threads.
        
        This method ensures all background threads are properly stopped
        before the application closes, preventing QThread warnings.
        
        Args:
            event: Close event.
        """
        logger.info("Closing application...")
        
        # Wait for all workers to finish
        for worker in self._workers:
            if worker.isRunning():
                worker.wait(1000)  # Wait up to 1 second per worker
        
        event.accept()
