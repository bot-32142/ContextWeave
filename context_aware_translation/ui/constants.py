"""Constants for the UI module."""

import tomllib
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Final

from context_aware_translation.languages import (
    LANGUAGES,
    display_target_language_name,
    storage_target_language_name,
)

__all__ = ("LANGUAGES", "display_target_language_name", "storage_target_language_name")


def _application_version() -> str:
    """Return the source version in development and installed metadata in builds."""
    source_pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
    try:
        project = tomllib.loads(source_pyproject.read_text(encoding="utf-8")).get("project")
    except (OSError, tomllib.TOMLDecodeError):
        project = None
    if isinstance(project, dict):
        source_version = project.get("version")
        if isinstance(source_version, str) and source_version:
            return source_version
    try:
        return version("context-aware-translation")
    except PackageNotFoundError:  # pragma: no cover - only possible in malformed bundles
        return "unknown"


APP_VERSION: Final[str] = _application_version()

# Default window dimensions
DEFAULT_WINDOW_WIDTH: Final[int] = 1120
DEFAULT_WINDOW_HEIGHT: Final[int] = 760
MIN_WINDOW_WIDTH: Final[int] = 800
MIN_WINDOW_HEIGHT: Final[int] = 600

# Sidebar width
SIDEBAR_WIDTH: Final[int] = 280

# Table defaults
DEFAULT_PAGE_SIZE: Final[int] = 50
