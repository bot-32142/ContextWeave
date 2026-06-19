"""Hardcoded prompt guidance for specific source/target language pairs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from context_aware_translation.languages import storage_target_language_name
from context_aware_translation.llm.language_pair_prompts.japanese_to_simplified_chinese import (
    NAME_TRANSLATION_PROMPT,
    TRANSLATION_PROMPT,
)

PromptKind = Literal["translation", "name_translation"]


@dataclass(frozen=True)
class LanguagePairPromptPolicy:
    """Optional prompt additions for one canonical language pair."""

    translation: str | None = None
    name_translation: str | None = None


_JAPANESE_TO_SIMPLIFIED_CHINESE_POLICY = LanguagePairPromptPolicy(
    translation=TRANSLATION_PROMPT,
    name_translation=NAME_TRANSLATION_PROMPT,
)

_LANGUAGE_PAIR_PROMPT_POLICIES: dict[tuple[str, str], LanguagePairPromptPolicy] = {
    ("日语", "简体中文"): _JAPANESE_TO_SIMPLIFIED_CHINESE_POLICY,
}


def get_language_pair_prompt_policy(
    source_language: str,
    target_language: str,
) -> LanguagePairPromptPolicy | None:
    """Return a registered policy, normalizing known preset labels first."""
    canonical_source = storage_target_language_name(source_language) or source_language.strip()
    canonical_target = storage_target_language_name(target_language) or target_language.strip()
    return _LANGUAGE_PAIR_PROMPT_POLICIES.get((canonical_source, canonical_target))


def apply_language_pair_prompt_policy(
    prompt: str,
    *,
    source_language: str,
    target_language: str,
    prompt_kind: PromptKind,
    before_marker: str,
) -> str:
    """Insert registered guidance, leaving unregistered prompts unchanged."""
    policy = get_language_pair_prompt_policy(source_language, target_language)
    if policy is None:
        return prompt

    guidance = policy.translation if prompt_kind == "translation" else policy.name_translation
    if not guidance:
        return prompt
    if before_marker not in prompt:
        raise ValueError(f"Prompt insertion marker not found: {before_marker}")
    return prompt.replace(before_marker, f"{guidance}\n\n{before_marker}", 1)
