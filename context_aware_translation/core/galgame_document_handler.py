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
        """Use the normal chunk concatenation and newline split behavior."""
        return manager.get_translated_lines(document_id)
