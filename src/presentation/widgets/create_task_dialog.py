"""Dialog for creating a new task.

This module provides a dialog for creating tasks with title and description.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class CreateTaskDialog(QDialog):
    """Dialog for creating a new task.

    Args:
        parent: Parent widget.
    """

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Create New Task")
        self.setMinimumWidth(400)
        self.setModal(True)

        self._setup_ui()
        self._apply_styles()

    def _setup_ui(self) -> None:
        """Set up the user interface components."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Title label
        title_label = QLabel("Create New Task")
        title_label.setObjectName("dialogTitleLabel")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setWeight(QFont.Weight.Bold)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        # Task title input
        title_input_layout = QVBoxLayout()
        title_input_layout.setSpacing(8)

        title_label = QLabel("Title *")
        title_label.setObjectName("fieldLabel")
        title_input_layout.addWidget(title_label)

        self._title_input = QLineEdit()
        self._title_input.setObjectName("taskTitleInput")
        self._title_input.setPlaceholderText("Enter task title...")
        self._title_input.setFixedHeight(40)
        title_input_layout.addWidget(self._title_input)

        layout.addLayout(title_input_layout)

        # Task description input
        desc_input_layout = QVBoxLayout()
        desc_input_layout.setSpacing(8)

        desc_label = QLabel("Description (optional)")
        desc_label.setObjectName("fieldLabel")
        desc_input_layout.addWidget(desc_label)

        self._description_input = QTextEdit()
        self._description_input.setObjectName("taskDescriptionInput")
        self._description_input.setPlaceholderText("Enter task description...")
        self._description_input.setFixedHeight(80)
        desc_input_layout.addWidget(self._description_input)

        layout.addLayout(desc_input_layout)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Cancel |
            QDialogButtonBox.StandardButton.Ok
        )
        button_box.setObjectName("dialogButtonBox")
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        # Style buttons
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setText("Create Task")
        ok_button.setObjectName("createTaskButton")
        ok_button.setFixedHeight(40)

        cancel_button = button_box.button(QDialogButtonBox.StandardButton.Cancel)
        cancel_button.setText("Cancel")
        cancel_button.setObjectName("cancelButton")
        cancel_button.setFixedHeight(40)

        layout.addWidget(button_box)

    def _apply_styles(self) -> None:
        """Apply Qt Style Sheets."""
        self.setStyleSheet("""
            /* Dialog */
            QDialog {
                background-color: #1A1A1A;
            }

            /* Title */
            QLabel#dialogTitleLabel {
                color: #FFFFFF;
                padding-bottom: 8px;
            }

            /* Field labels */
            QLabel#fieldLabel {
                color: #A0A0A0;
                font-size: 13px;
                font-weight: 500;
            }

            /* Title input */
            QLineEdit#taskTitleInput {
                background-color: #242424;
                border: 1px solid #6B6B6B;
                border-radius: 8px;
                padding: 10px 14px;
                color: #FFFFFF;
                font-size: 14px;
            }

            QLineEdit#taskTitleInput:focus {
                border: 2px solid #8B5CF6;
                background-color: #242424;
            }

            QLineEdit#taskTitleInput::placeholder {
                color: #6B6B6B;
            }

            /* Description input */
            QTextEdit#taskDescriptionInput {
                background-color: #242424;
                border: 1px solid #6B6B6B;
                border-radius: 8px;
                padding: 10px 14px;
                color: #FFFFFF;
                font-size: 14px;
            }

            QTextEdit#taskDescriptionInput:focus {
                border: 2px solid #8B5CF6;
                background-color: #242424;
            }

            QTextEdit#taskDescriptionInput::placeholder {
                color: #6B6B6B;
            }

            /* Create button */
            QPushButton#createTaskButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8B5CF6, stop:1 #7C3AED);
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                color: #FFFFFF;
                font-size: 14px;
                font-weight: 600;
            }

            QPushButton#createTaskButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9B6CF6, stop:1 #8C4AED);
            }

            QPushButton#createTaskButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7C3AED, stop:1 #6D28D9);
            }

            /* Cancel button */
            QPushButton#cancelButton {
                background-color: #242424;
                border: 1px solid #6B6B6B;
                border-radius: 8px;
                padding: 12px 24px;
                color: #A0A0A0;
                font-size: 14px;
            }

            QPushButton#cancelButton:hover {
                background-color: #333333;
                border: 1px solid #888888;
                color: #FFFFFF;
            }
        """)

    def get_result(self) -> tuple[str, str | None]:
        """Get the task title and description.

        Returns:
            Tuple of (title, description). Description can be None.
        """
        title = self._title_input.text().strip()
        description = self._description_input.toPlainText().strip()
        return title, description if description else None
