"""Dialog for editing task details.

This module provides a modal dialog for editing task title and description.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTextEdit,
    QVBoxLayout,
)


class EditTaskDialog(QDialog):
    """Modal dialog for editing task details.
    
    This dialog allows users to modify the title and description
    of an existing task.
    """

    def __init__(self, title: str, description: str | None,
                 parent=None):
        """Initialize the edit task dialog.
        
        Args:
            title: Current task title.
            description: Current task description.
            parent: Parent widget.
        """
        super().__init__(parent)

        self._title = title
        self._description = description or ""
        self._result_title = ""
        self._result_description = ""

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        self.setWindowTitle("Edit Task")
        self.setModal(True)
        self.setMinimumWidth(400)
        self.setMinimumHeight(300)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(10)

        # Title input
        self._title_input = QLineEdit(self._title)
        self._title_input.setPlaceholderText("Enter task title...")
        self._title_input.setMaxLength(200)
        title_font = QFont()
        title_font.setPointSize(11)
        self._title_input.setFont(title_font)
        form_layout.addRow("Title:", self._title_input)

        # Description input
        self._description_input = QTextEdit()
        self._description_input.setPlaceholderText("Enter task description (optional)...")
        self._description_input.setText(self._description)
        self._description_input.setMinimumHeight(150)
        desc_font = QFont()
        desc_font.setPointSize(10)
        self._description_input.setFont(desc_font)
        form_layout.addRow("Description:", self._description_input)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setFixedWidth(80)
        button_layout.addWidget(cancel_btn)

        button_layout.addSpacerItem(QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        ))

        save_btn = QPushButton("Save")
        save_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        save_btn.clicked.connect(self._on_save_clicked)
        save_btn.setFixedWidth(80)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets for modern appearance."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 11px;
            }
            QLineEdit {
                background-color: #3e3e3e;
                border: 1px solid #505050;
                border-radius: 4px;
                padding: 8px;
                color: #e0e0e0;
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 1px solid #4a9eff;
            }
            QTextEdit {
                background-color: #3e3e3e;
                border: 1px solid #505050;
                border-radius: 4px;
                padding: 8px;
                color: #e0e0e0;
                font-size: 10px;
            }
            QTextEdit:focus {
                border: 1px solid #4a9eff;
            }
            QPushButton {
                background-color: #3e3e3e;
                border: 1px solid #505050;
                border-radius: 4px;
                padding: 8px 16px;
                color: #e0e0e0;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border: 1px solid #6a6a6a;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
        """)

    def _on_save_clicked(self) -> None:
        """Handle save button click."""
        title = self._title_input.text().strip()
        description = self._description_input.toPlainText().strip()

        if not title:
            self._title_input.setStyleSheet(
                "QLineEdit { background-color: #5a2a2a; border: 1px solid #7a3a3a; }"
            )
            return

        self._result_title = title
        self._result_description = description if description else None
        self.accept()

    def get_result(self) -> tuple[str, str | None]:
        """Get the edited title and description.
        
        Returns:
            tuple[str, str | None]: Tuple of (title, description).
        """
        return self._result_title, self._result_description
