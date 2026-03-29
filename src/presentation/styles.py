"""Application style sheets based on the design system.

This module provides QSS styles following the Obsidian × Spotify design philosophy.
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


def get_main_window_styles() -> str:
    """Get styles for the main application window.
    
    Returns:
        str: QSS stylesheet for QMainWindow.
    """
    return f"""
    QMainWindow {{
        background-color: {COLORS['void_black']};
    }}
    
    QTabWidget::pane {{
        border: none;
        background-color: {COLORS['void_black']};
    }}
    
    QTabBar::tab {{
        background-color: {COLORS['surface_dark']};
        color: {COLORS['muted_gray']};
        padding: 14px 28px;
        border: none;
        border-bottom: 2px solid transparent;
        font-size: 13px;
        font-weight: 500;
        min-width: 100px;
    }}
    
    QTabBar::tab:selected {{
        background-color: {COLORS['void_black']};
        color: {COLORS['pure_white']};
        border-bottom: 2px solid {COLORS['nebula_purple']};
    }}
    
    QTabBar::tab:hover:!selected {{
        background-color: {COLORS['surface_light']};
        color: {COLORS['pure_white']};
    }}
    
    QTabBar::tab:first {{
        border-top-left-radius: 8px;
    }}
    
    QScrollArea {{
        border: none;
        background-color: {COLORS['void_black']};
    }}
    
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
    """


def get_task_item_styles() -> str:
    """Get styles for TaskItemWidget.
    
    Returns:
        str: QSS stylesheet for task items.
    """
    return f"""
    /* Task Card - Based on design.md */
    QFrame {{
        background-color: {COLORS['surface_dark']};
        border-radius: 8px;
        border: 1px solid {COLORS['surface_light']};
    }}
    
    QFrame:hover {{
        border: 1px solid {COLORS['dim_gray']};
    }}
    
    /* Checkbox Styling - Fixed artifacts */
    QCheckBox {{
        spacing: 10px;
    }}
    
    QCheckBox::indicator {{
        width: 20px;
        height: 20px;
        border-radius: 5px;
        border: 2px solid {COLORS['dim_gray']};
        background-color: {COLORS['surface_light']};
    }}
    
    QCheckBox::indicator:hover {{
        border: 2px solid {COLORS['lavender_glow']};
        background-color: {COLORS['surface_light']};
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {COLORS['success_green']};
        border: 2px solid {COLORS['success_green']};
    }}
    
    QCheckBox::indicator:checked:hover {{
        background-color: #059669;
        border: 2px solid #059669;
    }}
    
    QCheckBox::indicator:disabled {{
        background-color: {COLORS['surface_dark']};
        border: 2px solid {COLORS['surface_light']};
    }}
    
    /* Labels - No background artifacts */
    QLabel, QLabel#titleLabel, QLabel#dateLabel {{
        color: {COLORS['pure_white']};
        background-color: transparent;
        border: none;
    }}
    
    QLabel#dateLabel {{
        color: {COLORS['muted_gray']};
        font-size: 11px;
    }}
    
    /* Buttons */
    QPushButton {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 8px 16px;
        color: {COLORS['pure_white']};
        font-size: 12px;
        font-weight: 500;
    }}
    
    QPushButton:hover {{
        background-color: {COLORS['dim_gray']};
        border: 1px solid {COLORS['muted_gray']};
    }}
    
    QPushButton:pressed {{
        background-color: {COLORS['surface_dark']};
    }}
    
    QPushButton#deleteButton {{
        background-color: {COLORS['surface_light']};
        border: 1px solid #4A2B2B;
        color: {COLORS['error_red']};
    }}
    
    QPushButton#deleteButton:hover {{
        background-color: #3D2323;
        border: 1px solid #5A3535;
    }}
    
    QPushButton#reopenButton {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        color: {COLORS['success_green']};
    }}
    
    QPushButton#reopenButton:hover {{
        background-color: {COLORS['dim_gray']};
        border: 1px solid {COLORS['muted_gray']};
    }}
    """


def get_active_tasks_view_styles() -> str:
    """Get styles for ActiveTasksView.

    Returns:
        str: QSS stylesheet for active tasks view.
    """
    return f"""
    /* Active Tasks View - Based on design.md */
    QWidget {{
        background-color: {COLORS['void_black']};
    }}

    QLabel, QLabel#headerLabel {{
        color: {COLORS['pure_white']};
        background-color: transparent;
    }}

    QLabel#headerLabel {{
        font-size: 24px;
        font-weight: 600;
    }}

    /* Input Field */
    QLineEdit {{
        background-color: {COLORS['surface_dark']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 8px;
        padding: 12px 16px;
        color: {COLORS['pure_white']};
        font-size: 13px;
    }}

    QLineEdit:focus {{
        border: 2px solid {COLORS['nebula_purple']};
        background-color: {COLORS['surface_dark']};
    }}

    QLineEdit::placeholder {{
        color: {COLORS['muted_gray']};
    }}

    /* Add Button with Gradient */
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

    /* Scroll Area */
    QScrollArea {{
        border: none;
        background-color: {COLORS['void_black']};
    }}
    """


def get_date_group_styles() -> str:
    """Get styles for DateGroupWidget.

    Returns:
        str: QSS stylesheet for date groups.
    """
    return f"""
    /* Date Group Widget - Based on design.md */
    QFrame {{
        background-color: {COLORS['surface_dark']};
        border-radius: 8px;
        border: 1px solid {COLORS['surface_light']};
    }}

    QFrame:hover {{
        border: 1px solid {COLORS['dim_gray']};
    }}

    QLabel, QLabel#indicatorLabel {{
        color: {COLORS['pure_white']};
        background-color: transparent;
        border: none;
    }}

    QLabel#indicatorLabel {{
        color: {COLORS['muted_gray']};
        font-size: 12px;
    }}
    
    QLabel#dateHeaderTitle {{
        font-size: 14px;
        font-weight: 600;
    }}
    
    QLabel#dateHeaderCount {{
        color: {COLORS['muted_gray']};
        font-size: 12px;
    }}
    """


def get_edit_dialog_styles() -> str:
    """Get styles for EditTaskDialog.

    Returns:
        str: QSS stylesheet for edit dialog.
    """
    return f"""
    /* Edit Task Dialog - Based on design.md */
    QDialog {{
        background-color: {COLORS['surface_dark']};
        border-radius: 12px;
    }}

    QLabel {{
        color: {COLORS['pure_white']};
        font-size: 12px;
        font-weight: 500;
        background-color: transparent;
    }}

    QLineEdit {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 10px 14px;
        color: {COLORS['pure_white']};
        font-size: 13px;
    }}

    QLineEdit:focus {{
        border: 1px solid {COLORS['nebula_purple']};
        background-color: {COLORS['surface_light']};
    }}

    QTextEdit {{
        background-color: {COLORS['surface_light']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 6px;
        padding: 10px 14px;
        color: {COLORS['pure_white']};
        font-size: 12px;
    }}

    QTextEdit:focus {{
        border: 1px solid {COLORS['nebula_purple']};
        background-color: {COLORS['surface_light']};
    }}

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
        background-color: {COLORS['nebula_purple']};
        border: none;
    }}

    QPushButton#saveButton:hover {{
        background-color: {COLORS['deep_violet']};
    }}

    QPushButton#cancelButton {{
        background-color: transparent;
        border: 1px solid {COLORS['dim_gray']};
    }}

    QPushButton#cancelButton:hover {{
        background-color: {COLORS['surface_light']};
    }}
    """


def get_global_styles() -> str:
    """Get global application styles.

    Returns:
        str: Combined QSS stylesheet for the entire application.
    """
    return f"""
    /* Global Styles - Based on design.md */
    * {{
        font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }}

    QWidget {{
        color: {COLORS['pure_white']};
        background-color: transparent;
    }}

    /* QMainWindow */
    QMainWindow {{
        background-color: {COLORS['void_black']};
    }}

    /* QTabWidget - Fixed for dark theme */
    QTabWidget::pane {{
        border: none;
        background-color: {COLORS['void_black']};
    }}

    QTabBar {{
        background-color: {COLORS['void_black']};
    }}

    QTabBar::tab {{
        background-color: {COLORS['surface_dark']};
        color: {COLORS['muted_gray']};
        padding: 14px 28px;
        border: none;
        border-bottom: 2px solid transparent;
        font-size: 13px;
        font-weight: 500;
        min-width: 100px;
        border-top-left-radius: 8px;
        border-top-right-radius: 8px;
    }}

    QTabBar::tab:selected {{
        background-color: {COLORS['void_black']};
        color: {COLORS['pure_white']};
        border-bottom: 2px solid {COLORS['nebula_purple']};
    }}

    QTabBar::tab:hover:!selected {{
        background-color: {COLORS['surface_light']};
        color: {COLORS['pure_white']};
    }}

    /* QScrollArea */
    QScrollArea {{
        border: none;
        background-color: {COLORS['void_black']};
    }}

    /* QScrollBar - Dark theme */
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

    /* QMessageBox */
    QMessageBox {{
        background-color: {COLORS['surface_dark']};
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

    /* QToolTip */
    QToolTip {{
        background-color: {COLORS['surface_light']};
        color: {COLORS['pure_white']};
        border: 1px solid {COLORS['dim_gray']};
        border-radius: 4px;
        padding: 6px 10px;
        font-size: 12px;
    }}

    /* QMenu */
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
    """
