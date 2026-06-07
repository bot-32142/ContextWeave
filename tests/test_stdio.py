from __future__ import annotations

import io
from unittest.mock import patch

from context_aware_translation.stdio import configure_standard_streams


def test_configure_standard_streams_allows_unicode_on_gbk_streams() -> None:
    stdout_buffer = io.BytesIO()
    stderr_buffer = io.BytesIO()
    stdout = io.TextIOWrapper(stdout_buffer, encoding="gbk", errors="strict")
    stderr = io.TextIOWrapper(stderr_buffer, encoding="gbk", errors="strict")

    with patch("context_aware_translation.stdio.sys.stdout", stdout), patch(
        "context_aware_translation.stdio.sys.stderr", stderr
    ):
        configure_standard_streams()
        print("Alice・Bob", file=stdout)
        print("Error: Alice・Bob", file=stderr)
        stdout.flush()
        stderr.flush()

    assert stdout_buffer.getvalue().decode("utf-8").strip() == "Alice・Bob"
    assert stderr_buffer.getvalue().decode("utf-8").strip() == "Error: Alice・Bob"
