from __future__ import annotations

import pytest

from context_aware_translation.core.galgame_document_handler import GalgameDocumentHandler
from context_aware_translation.storage.schema.book_db import TranslationChunkRecord


class DummyTermRepo:
    def __init__(self, chunks: list[TranslationChunkRecord]) -> None:
        self._chunks = chunks

    def list_chunks(self, document_id: int | None = None) -> list[TranslationChunkRecord]:
        if document_id is None:
            return list(self._chunks)
        return [chunk for chunk in self._chunks if chunk.document_id == document_id]


class DummyManager:
    def __init__(self, chunks: list[TranslationChunkRecord] | None = None) -> None:
        self.add_text_calls: list[tuple[str, int, int]] = []
        self.translate_calls: list[dict[str, object]] = []
        self.term_repo = DummyTermRepo(chunks or [])

    def add_text(self, text: str, max_token_size_per_chunk: int, document_id: int) -> int:
        self.add_text_calls.append((text, max_token_size_per_chunk, document_id))
        return 42

    async def translate_chunks(self, **kwargs):  # noqa: ANN003
        self.translate_calls.append(kwargs)


def test_galgame_handler_delegates_add_text_to_generic_pipeline() -> None:
    manager = DummyManager()
    handler = GalgameDocumentHandler()

    last_chunk_id = handler.add_text("こんにちは\nまたね", 500, 7, manager)

    assert last_chunk_id == 42
    assert manager.add_text_calls == [("こんにちは\nまたね", 500, 7)]


def test_galgame_handler_returns_source_line_aligned_translations() -> None:
    chunks = [
        TranslationChunkRecord(
            chunk_id=1,
            hash="hash-1",
            text="こんにちは\nまたね",
            document_id=7,
            is_translated=True,
            translation="你好 补一句\n再见",
        )
    ]
    manager = DummyManager(chunks)
    handler = GalgameDocumentHandler()

    assert handler.get_translated_lines(7, manager) == ["你好 补一句", "再见"]


def test_galgame_handler_rejects_translated_line_count_mismatch() -> None:
    chunks = [
        TranslationChunkRecord(
            chunk_id=1,
            hash="hash-1",
            text="こんにちは\nまたね",
            document_id=7,
            is_translated=True,
            translation="你好\n补一句\n再见",
        )
    ]
    manager = DummyManager(chunks)
    handler = GalgameDocumentHandler()

    with pytest.raises(ValueError, match="chunk 1 line count mismatch: expected 2, got 3"):
        handler.get_translated_lines(7, manager)


async def test_galgame_handler_delegates_translation_with_configured_batching() -> None:
    manager = DummyManager()
    handler = GalgameDocumentHandler(concurrency=3, batch_size=0, max_tokens_per_batch=1234)

    await handler.translate_chunks([7], manager, force=True)

    assert manager.translate_calls == [
        {
            "concurrency": 3,
            "batch_size": 0,
            "max_tokens_per_batch": 1234,
            "document_ids": [7],
            "force": True,
            "cancel_check": None,
            "progress_callback": None,
        }
    ]
