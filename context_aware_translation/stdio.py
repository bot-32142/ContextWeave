from __future__ import annotations

import sys
from typing import Any

_STANDARD_STREAM_ENCODING = "utf-8"
_STANDARD_STREAM_ERRORS = "backslashreplace"


def _configure_stream(stream: Any) -> None:
    if stream is None:
        return

    reconfigure = getattr(stream, "reconfigure", None)
    if not callable(reconfigure):
        return

    try:
        reconfigure(encoding=_STANDARD_STREAM_ENCODING, errors=_STANDARD_STREAM_ERRORS)
    except (AttributeError, LookupError, OSError, TypeError, ValueError):
        # Some embedded/frozen streams expose reconfigure but reject encoding changes.
        # If possible, still make encoding errors non-fatal on the existing codec.
        try:
            reconfigure(errors=_STANDARD_STREAM_ERRORS)
        except (AttributeError, LookupError, OSError, TypeError, ValueError):
            return


def configure_standard_streams() -> None:
    """Make process stdout/stderr safe for multilingual document text.

    Windows redirected streams can default to the locale code page (for example
    GBK). LLM previews, CLI JSON, and task errors routinely contain Japanese or
    other non-ASCII text, so configure Python's standard streams to emit UTF-8
    instead of letting ordinary print/log writes crash background work.
    """
    _configure_stream(sys.stdout)
    _configure_stream(sys.stderr)
