from __future__ import annotations

from context_aware_translation.core.galgame_document_handler import GalgameDocumentHandler


class DummyManager:
    def __init__(self) -> None:
        self.add_text_calls: list[tuple[str, int, int]] = []
        self.translate_calls: list[dict[str, object]] = []
        self.translated_lines = ["你好", "再见"]

    def add_text(self, text: str, max_token_size_per_chunk: int, document_id: int) -> int:
        self.add_text_calls.append((text, max_token_size_per_chunk, document_id))
        return 42

    async def translate_chunks(self, **kwargs):  # noqa: ANN003
        self.translate_calls.append(kwargs)

    def get_translated_lines(self, document_id: int) -> list[str]:
        assert document_id == 7
        return self.translated_lines


def test_galgame_handler_delegates_add_text_to_generic_pipeline() -> None:
    manager = DummyManager()
    handler = GalgameDocumentHandler()

    last_chunk_id = handler.add_text("こんにちは\nまたね", 500, 7, manager)

    assert last_chunk_id == 42
    assert manager.add_text_calls == [("こんにちは\nまたね", 500, 7)]


def test_galgame_handler_delegates_get_translated_lines_to_generic_pipeline() -> None:
    manager = DummyManager()
    handler = GalgameDocumentHandler()

    assert handler.get_translated_lines(7, manager) == ["你好", "再见"]


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
