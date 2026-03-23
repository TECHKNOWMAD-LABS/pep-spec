"""Shared constants and helpers for PEP conformance tests."""

from __future__ import annotations

import json
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

# Ensure project root is on sys.path so stubs can be imported.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

SCHEMAS_DIR = PROJECT_ROOT / "schemas"

# ── UUIDs used across tests ─────────────────────────────────────────────────

VALID_UUID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
VALID_UUID_2 = "b2c3d4e5-f6a7-8901-bcde-f12345678901"
VALID_UUID_3 = "c3d4e5f6-a7b8-9012-cdef-123456789012"
VALID_CHECKSUM = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
VALID_DATETIME = "2026-01-15T10:30:00Z"
VALID_SEMVER = "1.0.0"


@lru_cache(maxsize=16)
def load_schema(name: str) -> dict[str, Any]:
    """Load a JSON Schema file by base name (without extension).

    Cached via lru_cache — repeated calls for the same schema avoid
    redundant disk I/O and JSON parsing.
    """
    path = SCHEMAS_DIR / f"{name}.schema.json"
    with open(path) as f:
        return json.load(f)
