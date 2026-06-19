from __future__ import annotations

import pytest

from context_aware_translation.llm.glossary_translator import _build_batch_system_prompt
from context_aware_translation.llm.language_pair_prompts import (
    apply_language_pair_prompt_policy,
    get_language_pair_prompt_policy,
)
from context_aware_translation.llm.translator import build_translation_prompt


@pytest.mark.parametrize("source_language", ["日语", "日本語"])
@pytest.mark.parametrize("target_language", ["简体中文", "中文（简体）"])
def test_japanese_to_simplified_chinese_policy_resolves_preset_labels(
    source_language: str,
    target_language: str,
) -> None:
    assert get_language_pair_prompt_policy(source_language, target_language) is not None


@pytest.mark.parametrize("target_language", ["繁体中文", "中文（繁體）"])
def test_japanese_to_traditional_chinese_has_no_policy(target_language: str) -> None:
    assert get_language_pair_prompt_policy("日语", target_language) is None


def test_unregistered_pair_has_no_policy() -> None:
    assert get_language_pair_prompt_policy("英语", "简体中文") is None


@pytest.mark.parametrize(
    ("source_language", "target_language"),
    [("英语", "简体中文"), ("日语", "繁体中文")],
)
def test_unregistered_pair_leaves_prompt_byte_for_byte_unchanged(
    source_language: str,
    target_language: str,
) -> None:
    original = "generic prompt\n--marker--\n"

    result = apply_language_pair_prompt_policy(
        original,
        source_language=source_language,
        target_language=target_language,
        prompt_kind="translation",
        before_marker="--marker--",
    )

    assert result == original


def test_registered_pair_requires_a_valid_insertion_marker() -> None:
    with pytest.raises(ValueError, match="Prompt insertion marker not found"):
        apply_language_pair_prompt_policy(
            "generic prompt",
            source_language="日语",
            target_language="简体中文",
            prompt_kind="translation",
            before_marker="--missing--",
        )


def test_japanese_to_simplified_chinese_document_prompt_includes_special_guidance() -> None:
    system_prompt, _user_prompt = build_translation_prompt(
        ["彼は仕方なく頷いた。"],
        [],
        "日语",
        "简体中文",
    )

    assert "--日译简中专项要求--" in system_prompt
    assert "日中同形异义词" in system_prompt
    assert "日文标点转换为简体中文规范标点" in system_prompt
    assert system_prompt.index("--日译简中专项要求--") < system_prompt.index("--格式与标记（必须严格遵守）--")


def test_japanese_to_simplified_chinese_name_prompt_includes_special_guidance() -> None:
    prompt = _build_batch_system_prompt("日语", "简体中文")

    assert "---日语名称译简中专项要求---" in prompt
    assert "不得把姓名含义意译" in prompt
    assert prompt.index("---日语名称译简中专项要求---") < prompt.index("---示例---")


def test_other_pairs_do_not_receive_japanese_guidance() -> None:
    translation_prompt, _user_prompt = build_translation_prompt([], [], "英语", "简体中文")
    name_prompt = _build_batch_system_prompt("英语", "简体中文")

    assert "--日译简中专项要求--" not in translation_prompt
    assert "---日语名称译简中专项要求---" not in name_prompt
