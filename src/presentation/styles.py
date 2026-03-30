"""Application style sheets based on the design system.

This module provides QSS styles following the Obsidian × Spotify design philosophy.
All elements support transparency for custom background feature.
"""

# Color Palette from DESIGN.md
COLORS = {
    # Primary Colors
    "void_black": "#0D0D0D",
    "surface_dark": "#1A1A1A",
    "surface_light": "#242424",
    "pure_white": "#FFFFFF",
    "muted_gray": "#A0A0A0",
    "dim_gray": "#6B6B6B",

    # Accent Colors (Purple Family)
    "nebula_purple": "#8B5CF6",
    "deep_violet": "#7C3AED",
    "lavender_glow": "#A78BFA",
    "purple_mist": "#C4B5FD",

    # Semantic Colors
    "success_green": "#10B981",
    "warning_amber": "#F59E0B",
    "error_red": "#EF4444",
    "info_blue": "#3B82F6",
}


def get_global_styles(custom_background: bool = False) -> str:
    """Get global application styles.

    Args:
        custom_background: If True, make all backgrounds transparent.

    Returns:
        str: Combined QSS stylesheet for the entire application.
    """
    bg_color = "transparent" if custom_background else COLORS["void_black"]
    pane_bg = "transparent" if custom_background else COLORS["void_black"]

    return f"""
    /* ============================================
       GLOBAL STYLES - Obsidian × Spotify Design
       ============================================ */
    
    * {{
        font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    QWidget {{
        color: {COLORS['pure_white']};
        background-color: transparent;
    }}

    /* ============================================
       MAIN WINDOW
       ============================================ */
    QMainWindow {{
        background-color: {bg_color};
    }}

    QWidget#centralWidget {{
        background-color: transparent;
    }}

    /* ============================================
       TAB WIDGET PANE
       ============================================ */
    QTabWidget::pane {{
        border: none;
        background-color: {pane_bg};
    }}

    /* ============================================
       SCROLL AREAS
       ============================================ */
    QScrollArea {{
        border: none;
        background-color: transparent;
    }}

    QScrollArea > QWidget > QWidget {{
        background-color: transparent;
    }}

    /* ============================================
       SCROLL BAR - Dark theme
       ============================================ */
    QScrollBar:vertical {{
        background-color: {COLORS['surface_dark']};
        width: 10px;
        border-radius: 5px;
        margin: 0px;
    }}

    QScrollBar::handle:vertical {{
        background-color: {COLORS['dim_gray']};
        border-radius: 5px;
        min-height: 20px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {COLORS['muted_gray']};
    }}

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}

    QScrollBar:horizontal {{
        background-color: {COLORS['surface_dark']};
        height: 10px;
        border-radius: 5px;
        margin: 0px;
    }}

    QScrollBar::handle:horizontal {{
        background-color: {COLORS['dim_gray']};
        border-radius: 5px;
        min-width: 20px;
    }}

    QScrollBar::handle:horizontal:hover {{
        background-color: {COLORS['muted_gray']};
    }}

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        width: 0px;
    }}

    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: none;
    }}

    /* ============================================
       MESSAGE BOX
       ============================================ */
    QMessageBox {{
        background-color: {COLORS['surface_dark']};
        border-radius: 12px;
    }}

    QMessageBox QLabel {{
        color: {COLORS['pure_white']};
        font-size: 13px;
        background-color: transparent;
    }}

    QMessageBox QPushButton {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 8px 20px;
        color: {COLORS['pure_white']};
        font-size: 13px;
        min-width: 80px;
    }}

    QMessageBox QPushButton:hover {{
        background-color: {COLORS['dim_gray']};
    }}

    QMessageBox QPushButton:default {{
        background-color: {COLORS['nebula_purple']};
        border: none;
    }}

    QMessageBox QPushButton:default:hover {{
        background-color: {COLORS['deep_violet']};
    }}

    /* ============================================
       TOOLTIPS & MENUS
       ============================================ */
    QToolTip {{
        background-color: {COLORS['surface_light']};
        color: {COLORS['pure_white']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 4px;
        padding: 6px 10px;
        font-size: 12px;
    }}

    QMenu {{
        background-color: {COLORS['surface_dark']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 8px;
        padding: 6px 0;
    }}

    QMenu::item {{
        padding: 8px 20px;
        color: {COLORS['pure_white']};
    }}

    QMenu::item:selected {{
        background-color: {COLORS['surface_light']};
    }}

    QMenu::separator {{
        height: 1px;
        background-color: {COLORS['dim_gray']};
        margin: 6px 12px;
    }}

    /* ============================================
       GROUP BOX (Settings)
       ============================================ */
    QGroupBox {{
        background-color: transparent;
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 8px;
        margin-top: 12px;
        padding-top: 16px;
        font-size: 13px;
        font-weight: 600;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        subcontrol-position: top left;
        left: 12px;
        top: 0px;
        padding: 0 8px;
        color: {COLORS['muted_gray']};
    }}

    /* ============================================
       CHECKBOX (Settings)
       ============================================ */
    QCheckBox {{
        spacing: 10px;
        font-size: 13px;
    }}

    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border-radius: 4px;
        border: 2px solid {COLORS['dim_gray']};
        background-color: {COLORS['surface_light']};
    }}

    QCheckBox::indicator:hover {{
        border: 2px solid {COLORS['nebula_purple']};
    }}

    QCheckBox::indicator:checked {{
        background-color: {COLORS['nebula_purple']};
        border: 2px solid {COLORS['nebula_purple']};
    }}

    QCheckBox::indicator:checked:hover {{
        background-color: {COLORS['deep_violet']};
        border: 2px solid {COLORS['deep_violet']};
    }}

    /* ============================================
       LINE EDIT (Settings)
       ============================================ */
    QLineEdit {{
        background-color: {COLORS['surface_dark']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 10px 14px;
        color: {COLORS['pure_white']};
        font-size: 13px;
        min-height: 36px;
    }}

    QLineEdit:focus {{
        border: 1px solid {COLORS['nebula_purple']};
        background-color: {COLORS['surface_dark']};
    }}

    QLineEdit::placeholder {{
        color: {COLORS['muted_gray']};
    }}

    QLineEdit:disabled {{
        background-color: {COLORS['surface_dark']};
        color: {COLORS['dim_gray']};
    }}

    /* ============================================
       SLIDER (Opacity)
       ============================================ */
    QSlider::groove:horizontal {{
        border: none;
        height: 6px;
        background-color: {COLORS['surface_light']};
        border-radius: 3px;
    }}

    QSlider::handle:horizontal {{
        background-color: {COLORS['pure_white']};
        border: none;
        width: 18px;
        height: 18px;
        margin: -6px 0;
        border-radius: 9px;
    }}

    QSlider::handle:horizontal:hover {{
        background-color: {COLORS['nebula_purple']};
    }}

    QSlider::sub-page:horizontal {{
        background-color: {COLORS['nebula_purple']};
        border-radius: 3px;
    }}

    QSlider::add-page:horizontal {{
        background-color: {COLORS['surface_light']};
        border-radius: 3px;
    }}

    QSlider::tick {{
        background-color: {COLORS['dim_gray']};
    }}

    /* ============================================
       HEADER WITH TAB BUTTONS
       ============================================ */
    QWidget#headerWidget {{
        background-color: {COLORS['void_black']};
        border-bottom: 1px solid {COLORS['surface_light']};
    }}

    QPushButton#headerButton {{
        background-color: transparent;
        border: none;
        border-bottom: 2px solid transparent;
        color: {COLORS['muted_gray']};
        padding: 16px 24px;
        font-size: 14px;
        font-weight: 500;
        border-radius: 0;
    }}

    QPushButton#headerButton:hover {{
        background-color: {COLORS['surface_dark']};
        color: {COLORS['pure_white']};
    }}

    QPushButton#headerButton:checked {{
        background-color: {COLORS['surface_dark']};
        color: {COLORS['pure_white']};
        border-bottom: 2px solid {COLORS['nebula_purple']};
        font-weight: 600;
    }}

    /* ============================================
       BUTTONS (Settings)
       ============================================ */
    QPushButton {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 10px 20px;
        color: {COLORS['pure_white']};
        font-size: 13px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        background-color: {COLORS['dim_gray']};
        border: 1px solid {COLORS['muted_gray']};
    }}

    QPushButton:pressed {{
        background-color: {COLORS['surface_dark']};
    }}

    QPushButton#saveButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {COLORS['nebula_purple']}, stop:1 {COLORS['deep_violet']});
        border: none;
        font-weight: 600;
    }}

    QPushButton#saveButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #9B6CF6, stop:1 #8C4AED);
    }}

    QPushButton#saveButton:pressed {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {COLORS['deep_violet']}, stop:1 #6D28D9);
    }}

    QPushButton#browseButton {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 10px 16px;
        min-width: 80px;
    }}

    QPushButton#browseButton:hover {{
        background-color: {COLORS['dim_gray']};
    }}
    """


def get_active_tasks_view_styles(custom_background: bool = False) -> str:
    """Get styles for ActiveTasksView.

    Args:
        custom_background: If True, make all backgrounds transparent.

    Returns:
        str: QSS stylesheet for active tasks view.
    """
    return f"""
    /* ============================================
       ACTIVE TASKS VIEW
       ============================================ */
    QWidget#activeTasksView {{
        background-color: transparent;
    }}

    QLabel, QLabel#headerLabel {{
        color: {COLORS['pure_white']};
        background-color: transparent;
    }}

    QLabel#headerLabel {{
        font-size: 24px;
        font-weight: 600;
    }}

    /* ============================================
       INPUT FIELD
       ============================================ */
    QLineEdit#taskInput {{
        background-color: {COLORS['surface_dark']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 8px;
        padding: 12px 16px;
        color: {COLORS['pure_white']};
        font-size: 14px;
        min-height: 40px;
    }}

    QLineEdit#taskInput:focus {{
        border: 2px solid {COLORS['nebula_purple']};
        background-color: {COLORS['surface_dark']};
    }}

    QLineEdit#taskInput::placeholder {{
        color: {COLORS['muted_gray']};
    }}

    /* ============================================
       ADD BUTTON with Gradient
       ============================================ */
    QPushButton#addButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {COLORS['nebula_purple']}, stop:1 {COLORS['deep_violet']});
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        color: {COLORS['pure_white']};
        font-size: 13px;
        font-weight: 600;
    }}

    QPushButton#addButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #9B6CF6, stop:1 #8C4AED);
    }}

    QPushButton#addButton:pressed {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {COLORS['deep_violet']}, stop:1 #6D28D9);
    }}

    /* ============================================
       SCROLL AREA
       ============================================ */
    QScrollArea#tasksScrollArea {{
        border: none;
        background-color: transparent;
    }}
    """


def get_completed_tasks_view_styles() -> str:
    """Get styles for CompletedTasksView.

    Returns:
        str: QSS stylesheet for completed tasks view.
    """
    return f"""
    /* ============================================
       COMPLETED TASKS VIEW
       ============================================ */
    QWidget#completedTasksView {{
        background-color: transparent;
    }}

    QLabel, QLabel#headerLabel {{
        color: {COLORS['pure_white']};
        background-color: transparent;
    }}

    QLabel#headerLabel {{
        font-size: 24px;
        font-weight: 600;
    }}

    /* ============================================
       SCROLL AREA
       ============================================ */
    QScrollArea#completedScrollArea {{
        border: none;
        background-color: transparent;
    }}
    """


def get_task_item_styles(custom_background: bool = False) -> str:
    """Get styles for TaskItemWidget.

    Args:
        custom_background: If True, make all backgrounds transparent.

    Returns:
        str: QSS stylesheet for task items.
    """
    card_bg = "transparent" if custom_background else COLORS["surface_dark"]

    return f"""
    /* ============================================
       TASK CARD
       ============================================ */
    QFrame#taskCard {{
        background-color: {card_bg};
        border: 1px solid {COLORS['surface_light']};
        border-radius: 8px;
        padding: 0px;
    }}

    QFrame#taskCard:hover {{
        border: 1px solid {COLORS['dim_gray']};
    }}

    /* Inner container for transparency */
    QWidget#taskContent {{
        background-color: transparent;
    }}

    /* ============================================
       CHECKBOX - Fixed artifacts
       ============================================ */
    QCheckBox#taskCheckbox {{
        spacing: 10px;
    }}

    QCheckBox#taskCheckbox::indicator {{
        width: 20px;
        height: 20px;
        border-radius: 5px;
        border: 2px solid {COLORS['dim_gray']};
        background-color: {COLORS['surface_light']};
    }}

    QCheckBox#taskCheckbox::indicator:hover {{
        border: 2px solid {COLORS['lavender_glow']};
        background-color: {COLORS['surface_light']};
    }}

    QCheckBox#taskCheckbox::indicator:checked {{
        background-color: {COLORS['nebula_purple']};
        border: 2px solid {COLORS['nebula_purple']};
    }}

    QCheckBox#taskCheckbox::indicator:checked:hover {{
        background-color: {COLORS['deep_violet']};
        border: 2px solid {COLORS['deep_violet']};
    }}

    QCheckBox#taskCheckbox::indicator:disabled {{
        background-color: {COLORS['surface_dark']};
        border: 2px solid {COLORS['surface_light']};
    }}

    /* ============================================
       LABELS - No background artifacts
       ============================================ */
    QLabel, QLabel#titleLabel, QLabel#dateLabel, QLabel#charCountLabel {{
        color: {COLORS['pure_white']};
        background-color: transparent;
        border: none;
    }}

    QLabel#titleLabel {{
        font-size: 14px;
        font-weight: 500;
    }}

    QLabel#titleLabel:disabled {{
        color: {COLORS['muted_gray']};
    }}

    QLabel#dateLabel {{
        color: {COLORS['muted_gray']};
        font-size: 11px;
    }}

    QLabel#charCountLabel {{
        color: {COLORS['muted_gray']};
        font-size: 10px;
    }}

    /* ============================================
       BUTTONS
       ============================================ */
    QPushButton#editButton, QPushButton#deleteButton {{
        background-color: transparent;
        border: none;
        border-radius: 6px;
        padding: 6px 10px;
        color: {COLORS['muted_gray']};
        font-size: 16px;
    }}

    QPushButton#editButton:hover {{
        background-color: {COLORS['surface_light']};
        color: {COLORS['pure_white']};
    }}

    QPushButton#deleteButton:hover {{
        background-color: #3D2323;
        color: {COLORS['error_red']};
    }}

    QPushButton#reopenButton {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 6px 12px;
        color: {COLORS['success_green']};
        font-size: 12px;
    }}

    QPushButton#reopenButton:hover {{
        background-color: {COLORS['dim_gray']};
        border: 1px solid {COLORS['muted_gray']};
    }}
    """


def get_date_group_styles(custom_background: bool = False) -> str:
    """Get styles for DateGroupWidget.

    Args:
        custom_background: If True, make all backgrounds transparent.

    Returns:
        str: QSS stylesheet for date groups.
    """
    group_bg = "transparent" if custom_background else COLORS["surface_dark"]

    return f"""
    /* ============================================
       DATE GROUP WIDGET
       ============================================ */
    QFrame#dateGroupWidget {{
        background-color: {group_bg};
        border: 1px solid {COLORS['surface_light']};
        border-radius: 8px;
        margin: 4px 0;
    }}

    QFrame#dateGroupWidget:hover {{
        border: 1px solid {COLORS['dim_gray']};
    }}

    /* Inner content widget */
    QWidget#dateGroupContent {{
        background-color: transparent;
    }}

    /* ============================================
       HEADER
       ============================================ */
    QWidget#dateHeader {{
        background-color: transparent;
        padding: 4px;
    }}

    QLabel#dateHeaderTitle {{
        color: {COLORS['pure_white']};
        font-size: 13px;
        font-weight: 600;
        background-color: transparent;
    }}

    QLabel#dateHeaderCount {{
        color: {COLORS['muted_gray']};
        font-size: 12px;
        background-color: transparent;
        font-style: italic;
    }}

    QLabel#expandIndicator {{
        color: {COLORS['muted_gray']};
        font-size: 14px;
        background-color: transparent;
    }}

    /* ============================================
       TASKS CONTAINER
       ============================================ */
    QWidget#tasksContainer {{
        background-color: transparent;
    }}
    """


def get_edit_dialog_styles() -> str:
    """Get styles for EditTaskDialog.

    Returns:
        str: QSS stylesheet for edit dialog.
    """
    return f"""
    /* ============================================
       EDIT TASK DIALOG
       ============================================ */
    QDialog#editTaskDialog {{
        background-color: {COLORS['surface_dark']};
        border-radius: 12px;
    }}

    QLabel {{
        color: {COLORS['pure_white']};
        font-size: 12px;
        font-weight: 500;
        background-color: transparent;
    }}

    /* ============================================
       INPUT FIELDS
       ============================================ */
    QLineEdit#titleInput {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 10px 14px;
        color: {COLORS['pure_white']};
        font-size: 13px;
    }}

    QLineEdit#titleInput:focus {{
        border: 1px solid {COLORS['nebula_purple']};
        background-color: {COLORS['surface_light']};
    }}

    QLineEdit#titleInput::placeholder {{
        color: {COLORS['muted_gray']};
    }}

    QTextEdit#descriptionInput {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 10px 14px;
        color: {COLORS['pure_white']};
        font-size: 12px;
    }}

    QTextEdit#descriptionInput:focus {{
        border: 1px solid {COLORS['nebula_purple']};
        background-color: {COLORS['surface_light']};
    }}

    /* ============================================
       BUTTONS
       ============================================ */
    QPushButton {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 10px 20px;
        color: {COLORS['pure_white']};
        font-size: 13px;
        font-weight: 500;
    }}

    QPushButton:hover {{
        background-color: {COLORS['dim_gray']};
    }}

    QPushButton:pressed {{
        background-color: {COLORS['surface_dark']};
    }}

    QPushButton#saveButton {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 {COLORS['nebula_purple']}, stop:1 {COLORS['deep_violet']});
        border: none;
        font-weight: 600;
    }}

    QPushButton#saveButton:hover {{
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #9B6CF6, stop:1 #8C4AED);
    }}

    QPushButton#cancelButton {{
        background-color: transparent;
        border: 1px solid {COLORS['dim_gray']};
    }}

    QPushButton#cancelButton:hover {{
        background-color: {COLORS['surface_light']};
    }}
    """
