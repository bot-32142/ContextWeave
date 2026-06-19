from __future__ import annotations

import pytest

from context_aware_translation.languages import (
    display_target_language_name,
    require_storage_target_language_name,
    storage_target_language_name,
)


@pytest.mark.parametrize(
    ("value", "display_name", "storage_name"),
    [
        ("English", "English", "英语"),
        ("英语", "English", "英语"),
        ("日本語", "日本語", "日语"),
        ("日语", "日本語", "日语"),
    ],
)
def test_target_language_presets_normalize_to_display_and_storage_names(
    value: str,
    display_name: str,
    storage_name: str,
) -> None:
    assert display_target_language_name(value) == display_name
    assert storage_target_language_name(value) == storage_name


def test_unsupported_target_language_is_rejected() -> None:
    assert display_target_language_name("Klingon") is None
    assert storage_target_language_name("Klingon") is None
    with pytest.raises(ValueError, match="supported language presets"):
        require_storage_target_language_name("Klingon")
