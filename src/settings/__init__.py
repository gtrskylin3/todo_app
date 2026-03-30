"""Settings package for TODO Application.

This package provides settings management functionality:
- SettingsManager: Load/save settings to JSON
- SettingsDialog: UI for editing settings
"""

from src.settings.settings_manager import SettingsManager, AppSettings
from src.settings.settings_dialog import SettingsDialog

__all__ = ["SettingsManager", "AppSettings", "SettingsDialog"]
