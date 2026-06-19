"""Constants for the UI module."""

from typing import Final

from context_aware_translation.languages import (
    LANGUAGES,
    display_target_language_name,
    storage_target_language_name,
)

__all__ = ("LANGUAGES", "display_target_language_name", "storage_target_language_name")

# Application version
APP_VERSION: Final[str] = "0.1.1"

# Default window dimensions
DEFAULT_WINDOW_WIDTH: Final[int] = 1120
DEFAULT_WINDOW_HEIGHT: Final[int] = 760
MIN_WINDOW_WIDTH: Final[int] = 800
MIN_WINDOW_HEIGHT: Final[int] = 600

# Sidebar width
SIDEBAR_WIDTH: Final[int] = 280

# Table defaults
DEFAULT_PAGE_SIZE: Final[int] = 50
