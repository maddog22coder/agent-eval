"""Load JSON schemas shipped with the package."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_SCHEMA_DIR = Path(__file__).resolve().parent


@lru_cache(maxsize=4)
def get_conversation_schema() -> dict[str, Any]:
    """Return the conversation JSON schema as a Python dict."""
    schema_path = _SCHEMA_DIR / "conversation.schema.json"
    with schema_path.open(encoding="utf-8") as fh:
        result: dict[str, Any] = json.load(fh)
    return result
