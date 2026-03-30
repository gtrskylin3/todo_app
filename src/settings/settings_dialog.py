"""Settings dialog UI component.

This module provides a modal dialog for configuring application settings.
Independent from main application logic.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSlider,
    QCheckBox,
    QVBoxLayout,
    QWidget,
)

from src.presentation.styles import get_edit_dialog_styles
from src.settings.settings_manager import AppSettings


class SettingsDialog(QDialog):
    """Dialog for configuring application settings.
    
    This is a standalone UI component for settings management.
    """
    
    def __init__(self, settings: AppSettings, parent=None):
        """Initialize the settings dialog.
        
        Args:
            settings: Application settings to configure.
            parent: Parent widget.
        """
        super().__init__(parent)

        self._settings = settings
        self.setObjectName("editTaskDialog")
        self._setup_ui()
        self._apply_styles()
        self._load_settings()
    
    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        self.setWindowTitle("Settings")
        self.setMinimumWidth(450)
        self.setMinimumHeight(300)
        self.setModal(True)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)
        
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
        self._bg_image_input.setObjectName("titleInput")
        self._bg_image_input.setPlaceholderText("Select an image file...")
        self._bg_image_input.setReadOnly(True)
        path_layout.addWidget(self._bg_image_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.setObjectName("browseButton")
        browse_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self._on_browse_clicked)
        path_layout.addWidget(browse_btn)
        
        appearance_layout.addLayout(path_layout)
        
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
        opacity_layout.addWidget(self._opacity_slider)
        
        self._opacity_label = QLabel("100%")
        self._opacity_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        opacity_layout.addWidget(self._opacity_label)
        
        layout.addWidget(appearance_group)
        layout.addWidget(opacity_group)
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Reset button
        self._reset_btn = QPushButton("Reset to Defaults")
        self._reset_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._reset_btn.clicked.connect(self._on_reset_clicked)
        button_layout.addWidget(self._reset_btn)
        
        button_layout.addStretch()
        
        # Cancel button
        self._cancel_btn = QPushButton("Cancel")
        self._cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self._cancel_btn)
        
        # Save button
        self._save_btn = QPushButton("Save")
        self._save_btn.setObjectName("saveButton")
        self._save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._save_btn.clicked.connect(self._on_save_clicked)
        button_layout.addWidget(self._save_btn)
        
        layout.addLayout(button_layout)
    
    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets for modern appearance."""
        self.setStyleSheet(get_edit_dialog_styles())
    
    def _load_settings(self) -> None:
        """Load settings into UI controls."""
        # Appearance
        self._use_custom_bg_cb.setChecked(self._settings.appearance.use_custom_background)
        self._bg_image_input.setText(self._settings.appearance.background_image)
        self._bg_image_input.setEnabled(self._settings.appearance.use_custom_background)

        opacity_percent = int(self._settings.appearance.opacity * 100)
        self._opacity_slider.setValue(opacity_percent)
        self._opacity_label.setText(f"{opacity_percent}%")

        # Connect opacity slider
        self._opacity_slider.valueChanged.connect(self._on_opacity_changed)
    
    def _on_use_custom_bg_changed(self, state: int) -> None:
        """Handle custom background checkbox change."""
        self._bg_image_input.setEnabled(state == Qt.CheckState.Checked)
    
    def _on_browse_clicked(self) -> None:
        """Handle browse button click."""
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
    
    def _on_reset_clicked(self) -> None:
        """Handle reset button click."""
        from PyQt6.QtWidgets import QMessageBox

        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self._load_defaults()

    def _load_defaults(self) -> None:
        """Load default settings into UI."""
        self._use_custom_bg_cb.setChecked(False)
        self._bg_image_input.setText("")
        self._bg_image_input.setEnabled(False)

        self._opacity_slider.setValue(100)
        self._opacity_label.setText("100%")

    def _on_save_clicked(self) -> None:
        """Handle save button click."""
        # Save appearance settings
        self._settings.appearance.use_custom_background = self._use_custom_bg_cb.isChecked()
        self._settings.appearance.background_image = self._bg_image_input.text()
        self._settings.appearance.opacity = self._opacity_slider.value() / 100.0

        self.accept()

    def get_settings(self) -> AppSettings:
        """Get the configured settings."""
        return self._settings
