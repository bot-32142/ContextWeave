"""Shared product identity and legacy path helpers."""

from pathlib import Path

from platformdirs import user_config_dir, user_data_dir

APP_NAME = "ContextWeave"
APP_NAME_ZH = "语络译"
APP_ORGANIZATION_NAME = "ContextWeave"
APP_ORGANIZATION_DOMAIN = "contextweave"
APP_BUNDLE_IDENTIFIER = "com.contextweave.contextweave"
APP_DATA_DIR_NAME = "ContextWeave"
APP_TAGLINE = "Context-aware document translation"

LEGACY_APP_NAME = "Context-Aware Translation"
LEGACY_APP_ORGANIZATION_NAME = "CAT"
LEGACY_APP_DATA_DIR_NAME = "ContextAwareTranslation"


def default_user_data_dir() -> Path:
    """Return the app data directory, preserving existing legacy installs."""
    legacy_dir = Path(user_data_dir(LEGACY_APP_DATA_DIR_NAME, appauthor=False))
    if (legacy_dir / "registry.db").exists():
        return legacy_dir
    return Path(user_data_dir(APP_DATA_DIR_NAME, appauthor=False))


def default_user_config_dir() -> Path:
    """Return the app config directory, preserving an existing legacy CLI config."""
    legacy_dir = Path(user_config_dir(LEGACY_APP_DATA_DIR_NAME, appauthor=False))
    if (legacy_dir / "cli.yaml").exists():
        return legacy_dir
    return Path(user_config_dir(APP_DATA_DIR_NAME, appauthor=False))
