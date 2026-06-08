from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from context_aware_translation.core.cancellation import raise_if_cancelled

if TYPE_CHECKING:
    from context_aware_translation.core.context_manager import TranslationContextManager
    from context_aware_translation.core.progress import ProgressCallback


class GalgameDocumentHandler:
    """DocumentTypeHandler for galgame documents using the generic text pipeline."""

    def __init__(
        self,
        *,
        concurrency: int = 5,
        batch_size: int = 0,
        max_tokens_per_batch: int = 2000,
    ) -> None:
        self._concurrency = max(1, concurrency)
        self._batch_size = batch_size
        self._max_tokens_per_batch = max(1, max_tokens_per_batch)

    def add_text(
        self,
        text: str,
        max_token_size_per_chunk: int,
        document_id: int,
        manager: TranslationContextManager,
    ) -> int:
        """Let the normal semantic chunker group galgame text."""
        return manager.add_text(text, max_token_size_per_chunk, document_id)

    async def translate_chunks(
        self,
        document_ids: list[int],
        manager: TranslationContextManager,
        force: bool = False,
        source_ids: list[int] | None = None,
        cancel_check: Callable[[], bool] | None = None,
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        """Delegate to generic text translation with configured batching."""
        _ = source_ids
        raise_if_cancelled(cancel_check)
        await manager.translate_chunks(
            concurrency=self._concurrency,
            batch_size=self._batch_size,
            max_tokens_per_batch=self._max_tokens_per_batch,
            document_ids=document_ids,
            force=force,
            cancel_check=cancel_check,
            progress_callback=progress_callback,
        )

    def get_translated_lines(
        self,
        document_id: int,
        manager: TranslationContextManager,
    ) -> list[str]:
        """Return translated chunk text without global newline re-splitting.

        Galgame export is unit-aligned. A translated unit may legitimately
        contain an embedded newline, so the generic text export path would turn
        that one unit into multiple exported units and fail during patching.
        """
        chunks = manager.term_repo.list_chunks(document_id=document_id)
        if not chunks:
            raise ValueError("No chunks found in the database")

        sorted_chunks = sorted(chunks, key=lambda chunk: chunk.chunk_id)
        untranslated = [chunk for chunk in sorted_chunks if not chunk.is_translated or chunk.translation is None]
        if untranslated:
            untranslated_ids = [chunk.chunk_id for chunk in untranslated]
            raise ValueError(f"Cannot export: chunks {untranslated_ids} are not translated yet")

        lines: list[str] = []
        for chunk in sorted_chunks:
            if chunk.translation is None:
                continue
            lines.extend(_fit_translation_to_source_line_count(chunk.text, chunk.translation))
        return lines


def _fit_translation_to_source_line_count(source_text: str, translation: str) -> list[str]:
    source_line_count = len(_split_normalized_lines(source_text))
    translation_lines = _split_normalized_lines(translation)
    if source_line_count <= 1:
        return [translation.replace("\r\n", "\n").replace("\r", "\n")]
    if len(translation_lines) <= source_line_count:
        return translation_lines

    overflow_line_count = len(translation_lines) - source_line_count + 1
    return ["\n".join(translation_lines[:overflow_line_count]), *translation_lines[overflow_line_count:]]


def _split_normalized_lines(text: str) -> list[str]:
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
