from __future__ import annotations

from typing import Any


def json_object_response_format() -> dict[str, Any]:
    """Return the broadly supported JSON-mode request option."""
    return {"type": "json_object"}


def translation_json_schema_response_format() -> dict[str, Any]:
    """Return the strict schema used by translation and polish requests."""
    return {
        "type": "json_schema",
        "json_schema": {
            "name": "translation_response",
            "strict": True,
            "schema": {
                "type": "object",
                "properties": {
                    "翻译文本": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "id": {"type": "integer"},
                                "文本": {"type": "string"},
                            },
                            "required": ["id", "文本"],
                            "additionalProperties": False,
                        },
                    }
                },
                "required": ["翻译文本"],
                "additionalProperties": False,
            },
        },
    }
