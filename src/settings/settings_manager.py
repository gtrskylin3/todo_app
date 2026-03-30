"""Settings module for TODO Application.

This module provides settings management with JSON persistence.
Separate from core application logic.
"""

import json
import logging
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional


logger = logging.getLogger(__name__)


@dataclass
class WindowSettings:
    """Window-related settings."""
    width: int = 800
    height: int = 700
    x: int = -1
    y: int = -1
    maximized: bool = False


@dataclass
class AppearanceSettings:
    """Appearance-related settings."""
    background_image: str = ""
    use_custom_background: bool = False
    opacity: float = 1.0
    background_overlay_opacity: float = 0.6  # 60% overlay darkness


@dataclass
class BehaviorSettings:
    """Behavior-related settings."""
    minimize_to_tray: bool = False
    close_to_tray: bool = True
    start_minimized: bool = False
    show_notifications: bool = True


@dataclass
class AppSettings:
    """Main application settings container."""
    window: WindowSettings = None
    appearance: AppearanceSettings = None
    behavior: BehaviorSettings = None
    
    def __post_init__(self):
        if self.window is None:
            self.window = WindowSettings()
        if self.appearance is None:
            self.appearance = AppearanceSettings()
        if self.behavior is None:
            self.behavior = BehaviorSettings()
    
    def to_dict(self) -> dict:
        """Convert settings to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> "AppSettings":
        """Create settings from dictionary."""
        settings = cls()
        
        if "window" in data:
            settings.window = WindowSettings(**data["window"])
        
        if "appearance" in data:
            settings.appearance = AppearanceSettings(**data["appearance"])
        
        if "behavior" in data:
            settings.behavior = BehaviorSettings(**data["behavior"])
        
        return settings


class SettingsManager:
    """Manager for application settings with JSON persistence."""
    
    def __init__(self, settings_path: Optional[str] = None):
        """Initialize the settings manager.
        
        Args:
            settings_path: Optional path to settings file.
        """
        if settings_path:
            self._settings_file = Path(settings_path)
        else:
            # Default location: data/settings.json
            self._settings_file = Path(__file__).parent.parent.parent / "data" / "settings.json"
        
        self._settings = AppSettings()
        self.load()
    
    @property
    def settings(self) -> AppSettings:
        """Get current settings."""
        return self._settings
    
    @property
    def window(self) -> WindowSettings:
        """Get window settings."""
        return self._settings.window
    
    @property
    def appearance(self) -> AppearanceSettings:
        """Get appearance settings."""
        return self._settings.appearance
    
    @property
    def behavior(self) -> BehaviorSettings:
        """Get behavior settings."""
        return self._settings.behavior
    
    def load(self) -> None:
        """Load settings from file."""
        if not self._settings_file.exists():
            logger.info("Settings file not found, using defaults")
            return
        
        try:
            with open(self._settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self._settings = AppSettings.from_dict(data)
            logger.info(f"Settings loaded from {self._settings_file}")
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            self._settings = AppSettings()
    
    def save(self) -> None:
        """Save settings to file."""
        try:
            self._settings_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self._settings_file, "w", encoding="utf-8") as f:
                json.dump(self._settings.to_dict(), f, indent=2)
            
            logger.info(f"Settings saved to {self._settings_file}")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def reset(self) -> None:
        """Reset settings to defaults."""
        self._settings = AppSettings()
        self.save()
        logger.info("Settings reset to defaults")
