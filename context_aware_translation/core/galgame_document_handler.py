from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from context_aware_translation.core.cancellation import raise_if_cancelled
from context_aware_translation.documents.galgame import deserialize_translation_unit_stream
from context_aware_translation.storage.schema.book_db import ChunkRecord
from context_aware_translation.utils.hashing import compute_chunk_hash

if TYPE_CHECKING:
    from context_aware_translation.core.context_manager import TranslationContextManager
    from context_aware_translation.core.progress import ProgressCallback


class GalgameDocumentHandler:
    """DocumentTypeHandler for unit-preserving galgame translation."""

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
        max_token_size_per_chunk: int,  # noqa: ARG002
        document_id: int,
        manager: TranslationContextManager,
    ) -> int:
        """Store one chunk per translation unit without deduping repeated dialogue text."""
        units = deserialize_translation_unit_stream(text)
        chunk_records: list[ChunkRecord] = []
        chunk_id = manager.term_repo.get_next_chunk_id()
        for unit in units:
            if not unit.text.strip():
                continue
            identity_text = f"{unit.relative_path}\0{unit.unit_id}\0{unit.text}"
            chunk_records.append(
                ChunkRecord(
                    chunk_id=chunk_id,
                    hash=compute_chunk_hash(identity_text, document_id=document_id),
                    text=unit.text,
                    document_id=document_id,
                    is_extracted=False,
                    is_summarized=False,
                )
            )
            chunk_id += 1

        new_chunk_records = [
            chunk_record for chunk_record in chunk_records if not manager.term_repo.chunk_exists_by_hash(chunk_record.hash)
        ]
        if new_chunk_records:
            manager._state_update([], new_chunk_records)
        return chunk_id - 1

    async def translate_chunks(
        self,
        document_ids: list[int],
        manager: TranslationContextManager,
        force: bool = False,
        source_ids: list[int] | None = None,
        cancel_check: Callable[[], bool] | None = None,
        progress_callback: ProgressCallback | None = None,
    ) -> None:
        """Delegate to the generic text translator while preserving one chunk per unit."""
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
        """Return one translated entry per galgame translation unit."""
        chunks = manager.term_repo.list_chunks(document_id=document_id)
        if not chunks:
            raise ValueError("No chunks found in the database")

        sorted_chunks = sorted(chunks, key=lambda chunk: chunk.chunk_id)
        untranslated = [chunk for chunk in sorted_chunks if not chunk.is_translated or chunk.translation is None]
        if untranslated:
            untranslated_ids = [chunk.chunk_id for chunk in untranslated]
            raise ValueError(f"Cannot export: chunks {untranslated_ids} are not translated yet")
        return [chunk.translation for chunk in sorted_chunks if chunk.translation is not None]
