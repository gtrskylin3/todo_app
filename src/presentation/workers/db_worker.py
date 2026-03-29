"""Worker classes for background database operations.

This module provides QThread-based workers to execute database operations
without blocking the UI thread.
"""

from collections.abc import Callable
from typing import Any

from PyQt6.QtCore import QObject, QThread, pyqtSignal


class WorkerSignals(QObject):
    """Signals for worker thread communication.
    
    Attributes:
        finished: Emitted when the worker completes successfully.
        error: Emitted when an error occurs.
        result: Emitted with the operation result.
    """
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(object)


class DatabaseWorker(QThread):
    """Worker thread for executing database operations.
    
    This worker executes a callable function in a background thread
    and emits signals with the result or error.
    
    Args:
        fn: Callable function to execute.
        args: Positional arguments for the function.
        kwargs: Keyword arguments for the function.
    """

    def __init__(self, fn: Callable, *args: Any, **kwargs: Any):
        """Initialize the database worker.
        
        Args:
            fn: Function to execute in the background.
            *args: Positional arguments for the function.
            **kwargs: Keyword arguments for the function.
        """
        super().__init__()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs
        self.signals = WorkerSignals()

    def run(self) -> None:
        """Execute the function in the background thread."""
        try:
            result = self._fn(*self._args, **self._kwargs)
            self.signals.result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.signals.finished.emit()


class TaskOperationWorker(QThread):
    """Specialized worker for task operations.
    
    This worker is designed for task-specific database operations
    with typed result handling.
    
    Attributes:
        finished: Emitted when operation completes.
        error: Emitted with error message.
        task_result: Emitted with TaskServiceResult.
        tasks_result: Emitted with list of TaskEntity.
    """

    finished = pyqtSignal()
    error = pyqtSignal(str)
    task_result = pyqtSignal(object)  # TaskServiceResult
    tasks_result = pyqtSignal(object)  # list[TaskEntity]
    dates_result = pyqtSignal(object)  # list[datetime]

    def __init__(self, operation: Callable, *args: Any, **kwargs: Any):
        """Initialize the task operation worker.
        
        Args:
            operation: Function to execute.
            *args: Positional arguments.
            **kwargs: Keyword arguments.
        """
        super().__init__()
        self._operation = operation
        self._args = args
        self._kwargs = kwargs

    def run(self) -> None:
        """Execute the operation in the background thread."""
        try:
            result = self._operation(*self._args, **self._kwargs)

            # Emit appropriate signal based on result type
            if result is None:
                self.task_result.emit(None)
            elif hasattr(result, 'success'):
                # TaskServiceResult
                self.task_result.emit(result)
            elif isinstance(result, list):
                if result and hasattr(result[0], 'id'):
                    # list[TaskEntity]
                    self.tasks_result.emit(result)
                else:
                    # list[datetime] or empty
                    self.dates_result.emit(result)
            else:
                self.task_result.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
        finally:
            self.finished.emit()
