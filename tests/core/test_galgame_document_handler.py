from __future__ import annotations

from context_aware_translation.core.galgame_document_handler import GalgameDocumentHandler
from context_aware_translation.documents.galgame import TranslationUnit, serialize_translation_units
from context_aware_translation.storage.schema.book_db import ChunkRecord, TranslationChunkRecord


class DummyTermRepo:
    def __init__(self, chunks: list[ChunkRecord] | None = None) -> None:
        self._chunks = chunks or []

    def get_next_chunk_id(self) -> int:
        return max((chunk.chunk_id for chunk in self._chunks), default=-1) + 1

    def chunk_exists_by_hash(self, chunk_hash: str) -> int | None:
        for chunk in self._chunks:
            if chunk.hash == chunk_hash:
                return chunk.chunk_id
        return None

    def list_chunks(self, document_id: int | None = None) -> list[ChunkRecord]:
        if document_id is None:
            return list(self._chunks)
        return [chunk for chunk in self._chunks if chunk.document_id == document_id]


class DummyManager:
    def __init__(self, chunks: list[ChunkRecord] | None = None) -> None:
        self.term_repo = DummyTermRepo(chunks)
        self.translate_calls: list[dict[str, object]] = []

    def _state_update(self, extracted_keyed_context, chunk_records):  # noqa: ANN001, ARG002
        self.term_repo._chunks.extend(chunk_records)

    async def translate_chunks(self, **kwargs):  # noqa: ANN003
        self.translate_calls.append(kwargs)


def test_galgame_handler_add_text_preserves_repeated_dialogue_units() -> None:
    manager = DummyManager()
    handler = GalgameDocumentHandler()
    text = serialize_translation_units(
        [
            TranslationUnit(relative_path="script.json", unit_id="0", text="はい"),
            TranslationUnit(relative_path="script.json", unit_id="1", text="はい"),
        ]
    )

    last_chunk_id = handler.add_text(text, 100, 7, manager)

    chunks = manager.term_repo.list_chunks(document_id=7)
    assert last_chunk_id == 1
    assert [chunk.text for chunk in chunks] == ["はい", "はい"]
    assert chunks[0].hash != chunks[1].hash


def test_galgame_handler_get_translated_lines_preserves_multiline_units() -> None:
    chunks: list[ChunkRecord] = [
        TranslationChunkRecord(
            chunk_id=0,
            hash="h0",
            text="a",
            document_id=7,
            is_translated=True,
            translation="第一行\n第二行",
        ),
        TranslationChunkRecord(
            chunk_id=1,
            hash="h1",
            text="b",
            document_id=7,
            is_translated=True,
            translation="第三行",
        ),
    ]
    manager = DummyManager(chunks)
    handler = GalgameDocumentHandler()

    assert handler.get_translated_lines(7, manager) == ["第一行\n第二行", "第三行"]


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
