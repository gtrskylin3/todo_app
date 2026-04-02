"""Main window for the TODO application.

This module provides the MainWindow class which integrates all views
and handles the application logic with background threading.
"""

import logging

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QCloseEvent, QFont, QPixmap, QPalette
from PyQt6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSlider,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from src.application.task_service import TaskService, TaskServiceResult
from src.config.settings import AppConfig
from src.presentation.styles import get_active_tasks_view_styles, get_completed_tasks_view_styles, get_global_styles
from src.presentation.views.active_tasks_view import ActiveTasksView
from src.presentation.views.completed_tasks_view import CompletedTasksView
from src.presentation.views.today_tasks_view import TodayTasksView
from src.presentation.widgets.edit_task_dialog import EditTaskDialog
from src.presentation.workers.db_worker import DatabaseWorker
from src.settings import SettingsManager
from src.presentation.widgets.lofi_player import LofiPlayer

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
        self._settings_manager = SettingsManager()
        self._previous_tab_index = 0  # Track previous tab for settings
        self._bg_pixmap = None  # Custom background pixmap
        self._lofi_player = None  # LoFi player widget
        self._today_view = None  # Today tasks view

        self._setup_ui()
        self._apply_styles()
        self._apply_appearance_settings()  # Apply saved settings on startup
        self._load_initial_data()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        self.setWindowTitle(self._config.app_name)
        self.setMinimumSize(600, 700)

        # Central widget
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        # Main layout - this will hold the content
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Оставляем место для LoFi кнопки
        main_layout.setSpacing(0)

        # Header with tab buttons
        header_widget = self._create_header()
        main_layout.addWidget(header_widget)

        # Tab widget - hide default tab bar since we use custom header
        self._tab_widget = QTabWidget()
        self._tab_widget.setDocumentMode(True)
        self._tab_widget.tabBar().setVisible(False)
        self._tab_widget.currentChanged.connect(self._on_tab_changed)

        # Today tasks view (default tab)
        self._today_view = TodayTasksView()
        self._today_view.create_requested.connect(self._on_create_task)
        self._today_view.toggle_requested.connect(self._on_toggle_task)
        self._today_view.edit_requested.connect(self._on_edit_task)
        self._today_view.delete_requested.connect(self._on_delete_task)
        self._today_view.reopen_requested.connect(self._on_reopen_task)

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

        # Settings view
        self._settings_view = self._create_settings_view()

        self._tab_widget.addTab(self._today_view, "Today")
        self._tab_widget.addTab(self._active_view, "Active")
        self._tab_widget.addTab(self._completed_view, "Completed")
        self._tab_widget.addTab(self._settings_view, "Settings")

        main_layout.addWidget(self._tab_widget, 1)

        # Создаём LoFi плеер после setup_ui
        self._create_lofi_player()

    def _create_lofi_player(self) -> None:
        """Создать и позиционировать LoFi плеер в правом нижнем углу"""
        self._lofi_player = LofiPlayer(self)
        self._lofi_player.show()
        # Позиционируем после показа
        QTimer.singleShot(100, self._update_lofi_position)

    def _create_header(self) -> QWidget:
        """Create the header widget with tab buttons.

        Returns:
            QWidget: Header widget with navigation buttons.
        """
        header = QWidget()
        header.setObjectName("headerWidget")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Today button (default, first)
        self._today_btn = QPushButton("Today")
        self._today_btn.setObjectName("headerButton")
        self._today_btn.setCheckable(True)
        self._today_btn.setChecked(True)
        self._today_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._today_btn.clicked.connect(lambda: self._on_header_button_clicked(0))
        layout.addWidget(self._today_btn)

        # Active button
        self._active_btn = QPushButton("Active")
        self._active_btn.setObjectName("headerButton")
        self._active_btn.setCheckable(True)
        self._active_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._active_btn.clicked.connect(lambda: self._on_header_button_clicked(1))
        layout.addWidget(self._active_btn)

        # Completed button
        self._completed_btn = QPushButton("Completed")
        self._completed_btn.setObjectName("headerButton")
        self._completed_btn.setCheckable(True)
        self._completed_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._completed_btn.clicked.connect(lambda: self._on_header_button_clicked(2))
        layout.addWidget(self._completed_btn)

        # Settings button
        self._settings_btn = QPushButton("Settings")
        self._settings_btn.setObjectName("headerButton")
        self._settings_btn.setCheckable(True)
        self._settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._settings_btn.clicked.connect(lambda: self._on_header_button_clicked(3))
        layout.addWidget(self._settings_btn)

        return header

    def _update_lofi_position(self) -> None:
        """Позиционирует LoFi плеер в правом нижнем углу content area"""
        if self._lofi_player:
            margin = 0
            # Позиционируем относительно centralWidget
            central = self.centralWidget()
            if central:
                x = central.width() - self._lofi_player.width() - margin
                y = central.height() - self._lofi_player.height() - margin
                self._lofi_player.setParent(central)
                self._lofi_player.move(x, y)

    def resizeEvent(self, event) -> None:
        """Обработка изменения размера окна для обновления позиции LoFi и фона"""
        super().resizeEvent(event)
        self._update_lofi_position()

        # Обновляем фон при изменении размера
        settings = self._settings_manager.settings.appearance
        if settings.use_custom_background and settings.background_image:
            self._apply_custom_background(settings.background_image)

    def _on_header_button_clicked(self, index: int) -> None:
        """Handle header button click.

        Args:
            index: Index of the button (0=Today, 1=Active, 2=Completed, 3=Settings).
        """
        self._tab_widget.setCurrentIndex(index)
        # Update button states
        self._today_btn.setChecked(index == 0)
        self._active_btn.setChecked(index == 1)
        self._completed_btn.setChecked(index == 2)
        self._settings_btn.setChecked(index == 3)

    def _create_settings_view(self) -> QWidget:
        """Create the settings view widget.
        
        Returns:
            QWidget: Settings view widget.
        """
        widget = QWidget()
        widget.setObjectName("settingsView")
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Title
        title_label = QLabel("Settings")
        title_label.setObjectName("headerLabel")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setWeight(QFont.Weight.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # Appearance group
        appearance_group = QGroupBox("Appearance")
        appearance_layout = QVBoxLayout(appearance_group)
        appearance_layout.setSpacing(16)
        
        # Custom background checkbox
        self._use_custom_bg_cb = QCheckBox("Use custom background image")
        self._use_custom_bg_cb.setCursor(Qt.CursorShape.PointingHandCursor)
        self._use_custom_bg_cb.stateChanged.connect(self._on_use_custom_bg_changed)
        appearance_layout.addWidget(self._use_custom_bg_cb)
        
        # Background image path
        path_layout = QHBoxLayout()
        path_layout.setSpacing(8)
        
        self._bg_image_input = QLineEdit()
        self._bg_image_input.setPlaceholderText("Select an image file...")
        self._bg_image_input.setReadOnly(True)
        path_layout.addWidget(self._bg_image_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self._on_browse_clicked)
        path_layout.addWidget(browse_btn)
        
        appearance_layout.addLayout(path_layout)
        layout.addWidget(appearance_group)
        
        # Opacity group
        opacity_group = QGroupBox("Window Opacity")
        opacity_layout = QVBoxLayout(opacity_group)
        opacity_layout.setSpacing(12)
        
        self._opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self._opacity_slider.setMinimum(50)
        self._opacity_slider.setMaximum(100)
        self._opacity_slider.setSingleStep(5)
        self._opacity_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._opacity_slider.setTickInterval(10)
        self._opacity_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self._opacity_slider.valueChanged.connect(self._on_opacity_changed)
        opacity_layout.addWidget(self._opacity_slider)
        
        self._opacity_label = QLabel("100%")
        self._opacity_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        opacity_layout.addWidget(self._opacity_label)
        
        layout.addWidget(opacity_group)

        # Background overlay group
        overlay_group = QGroupBox("Background Overlay Darkness")
        overlay_layout = QVBoxLayout(overlay_group)
        overlay_layout.setSpacing(12)

        self._overlay_slider = QSlider(Qt.Orientation.Horizontal)
        self._overlay_slider.setMinimum(0)
        self._overlay_slider.setMaximum(100)
        self._overlay_slider.setSingleStep(5)
        self._overlay_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self._overlay_slider.setTickInterval(10)
        self._overlay_slider.setCursor(Qt.CursorShape.PointingHandCursor)
        self._overlay_slider.valueChanged.connect(self._on_overlay_changed)
        overlay_layout.addWidget(self._overlay_slider)

        self._overlay_label = QLabel("60%")
        self._overlay_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        overlay_layout.addWidget(self._overlay_label)

        layout.addWidget(overlay_group)
        layout.addStretch()
        
        # Save button
        save_btn = QPushButton("Save Settings")
        save_btn.setObjectName("saveButton")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.setFixedHeight(40)
        save_btn.clicked.connect(self._on_save_settings_clicked)
        layout.addWidget(save_btn)
        
        return widget

    def _on_tab_changed(self, index: int) -> None:
        """Handle tab change event.

        Args:
            index: Index of the selected tab.
        """
        # Показываем LoFi только на вкладке Today (index=0)
        if self._lofi_player:
            self._lofi_player.setVisible(index == 0)
            # Поднимаем кнопку выше контента
            if index == 0:
                self._lofi_player.raise_()

        if index == 3:  # Settings tab
            # Load current settings into UI
            self._load_settings_into_ui()

    def _load_settings_into_ui(self) -> None:
        """Load current settings into settings view UI controls."""
        settings = self._settings_manager.settings.appearance

        self._use_custom_bg_cb.setChecked(settings.use_custom_background)
        self._bg_image_input.setText(settings.background_image)
        self._bg_image_input.setEnabled(settings.use_custom_background)

        opacity_percent = int(settings.opacity * 100)
        self._opacity_slider.setValue(opacity_percent)
        self._opacity_label.setText(f"{opacity_percent}%")

        overlay_percent = int(settings.background_overlay_opacity * 100)
        self._overlay_slider.setValue(overlay_percent)
        self._overlay_label.setText(f"{overlay_percent}%")

    def _on_use_custom_bg_changed(self, state: int) -> None:
        """Handle custom background checkbox change."""
        self._bg_image_input.setEnabled(state == Qt.CheckState.Checked)

    def _on_browse_clicked(self) -> None:
        """Handle browse button click."""
        from PyQt6.QtWidgets import QFileDialog

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Background Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:
            self._bg_image_input.setText(file_path)

    def _on_opacity_changed(self, value: int) -> None:
        """Handle opacity slider change."""
        self._opacity_label.setText(f"{value}%")

    def _on_overlay_changed(self, value: int) -> None:
        """Handle overlay slider change."""
        self._overlay_label.setText(f"{value}%")

    def _on_save_settings_clicked(self) -> None:
        """Handle save settings button click."""
        # Save appearance settings
        self._settings_manager.settings.appearance.use_custom_background = self._use_custom_bg_cb.isChecked()
        self._settings_manager.settings.appearance.background_image = self._bg_image_input.text()
        self._settings_manager.settings.appearance.opacity = self._opacity_slider.value() / 100.0
        self._settings_manager.settings.appearance.background_overlay_opacity = self._overlay_slider.value() / 100.0
        self._settings_manager.save()
        
        # Apply settings immediately
        self._apply_appearance_settings()
        
        # Show confirmation
        QMessageBox.information(
            self,
            "Settings Saved",
            "Settings have been saved successfully."
        )

    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets for modern dark theme."""
        settings = self._settings_manager.settings.appearance
        use_custom_bg = settings.use_custom_background and settings.background_image

        # Only apply base styles if not using custom background
        # (custom background is applied separately in _apply_appearance_settings)
        if not use_custom_bg:
            self.setStyleSheet(get_global_styles(custom_background=False))
        
        self._active_view.setStyleSheet(get_active_tasks_view_styles(custom_background=use_custom_bg))
        self._completed_view.setStyleSheet(get_completed_tasks_view_styles())

    def _load_initial_data(self) -> None:
        """Load initial task data from the database."""
        self._load_today_tasks()
        self._load_active_tasks()
        self._load_completed_tasks()

    def _load_today_tasks(self) -> None:
        """Load today's tasks in a background thread."""
        def fetch_today():
            return self._task_service.get_todays_tasks()

        worker = DatabaseWorker(fetch_today)
        worker.signals.result.connect(self._on_today_tasks_loaded)
        worker.signals.error.connect(self._on_operation_error)
        worker.finished.connect(lambda: self._cleanup_worker(worker))
        self._workers.append(worker)
        worker.start()

    def _on_today_tasks_loaded(self, tasks) -> None:
        """Handle today's tasks loaded from database.

        Args:
            tasks: List of TaskEntity objects.
        """
        self._today_view.set_tasks(tasks)
        logger.debug(f"Loaded {len(tasks)} today's tasks")

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
            self._today_view.handle_operation_result(result, 'create')
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
            self._today_view.handle_operation_result(result, 'toggle', task_id)
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
            self._today_view.handle_operation_result(result, 'delete', task_id)
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

    def _apply_appearance_settings(self) -> None:
        """Apply appearance settings to the window."""
        settings = self._settings_manager.settings.appearance

        # Apply window opacity
        self.setWindowOpacity(settings.opacity)

        # Apply custom background image if enabled
        if settings.use_custom_background and settings.background_image:
            # Apply global styles with transparent backgrounds
            self.setStyleSheet(get_global_styles(custom_background=True))
            self._apply_custom_background(settings.background_image)
        else:
            # Reset to default styles
            self.setAutoFillBackground(False)
            self._bg_pixmap = None
            self.setStyleSheet(get_global_styles(custom_background=False))
            self.update()

        # Re-apply view-specific styles
        use_custom_bg = settings.use_custom_background and settings.background_image
        self._active_view.setStyleSheet(get_active_tasks_view_styles(custom_background=use_custom_bg))
        self._completed_view.setStyleSheet(get_completed_tasks_view_styles())
    
    
    def _apply_custom_background(self, image_path: str) -> None:
        """Apply custom background image with high quality scaling and overlay."""
        from PyQt6.QtGui import QPainter, QColor

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            logger.warning(f"Не удалось загрузить изображение: {image_path}")
            self._bg_pixmap = None
            return

        # Создаём итоговое изображение под размер окна
        result_pixmap = QPixmap(self.size())
        result_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(result_pixmap)
        
        # === ЭТИ СТРОКИ САМЫЕ ВАЖНЫЕ ДЛЯ УСТРАНЕНИЯ ПИКСЕЛЬНОСТИ ===
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        # ============================================================

        # Масштабируем картинку с высоким качеством
        scaled_pixmap = pixmap

        # Центрируем изображение
        x = (self.width() - scaled_pixmap.width()) // 2
        y = (self.height() - scaled_pixmap.height()) // 2

        painter.drawPixmap(x, y, scaled_pixmap)

        # Затемнение (overlay) — берём значение из настроек
        overlay_opacity = int(self._settings_manager.settings.appearance.background_overlay_opacity * 255)
        painter.setBrush(QColor(0, 0, 0, overlay_opacity))   # 0..255
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(result_pixmap.rect())

        painter.end()

        self._bg_pixmap = result_pixmap
        self.update()
    
    
    def paintEvent(self, event) -> None:
        from PyQt6.QtGui import QPainter

        painter = QPainter(self)
        
        if hasattr(self, '_bg_pixmap') and self._bg_pixmap and not self._bg_pixmap.isNull():
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, True)
            painter.drawPixmap(0, 0, self._bg_pixmap)

        super().paintEvent(event)   # важно вызывать в конце

    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle window close event to clean up threads.

        This method ensures all background threads are properly stopped
        before the application closes, preventing QThread warnings.

        Args:
            event: Close event.
        """
        logger.info("Closing application...")

        # Останавливаем LoFi
        if self._lofi_player:
            self._lofi_player.stop()

        # Wait for all workers to finish
        for worker in self._workers:
            if worker.isRunning():
                worker.wait(1000)  # Wait up to 1 second per worker

        event.accept()
