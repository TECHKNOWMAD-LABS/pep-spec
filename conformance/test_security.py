"""Security tests — path traversal, input injection, schema safety."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from conformance.helpers import load_schema
from stubs.validation import ValidationError, validate_string_not_empty, validate_uuid

# ── Path traversal prevention ────────────────────────────────────────────


class TestPathTraversal:
    def test_dotdot_rejected(self) -> None:
        load_schema.cache_clear()
        with pytest.raises(ValueError, match="path traversal"):
            load_schema("../../etc/passwd")

    def test_forward_slash_rejected(self) -> None:
        load_schema.cache_clear()
        with pytest.raises(ValueError, match="path traversal"):
            load_schema("foo/bar")

    def test_backslash_rejected(self) -> None:
        load_schema.cache_clear()
        with pytest.raises(ValueError, match="path traversal"):
            load_schema("foo\\bar")

    def test_valid_name_works(self) -> None:
        load_schema.cache_clear()
        schema = load_schema("organism")
        assert "$schema" in schema


# ── Input injection resistance ───────────────────────────────────────────


class TestInputInjection:
    def test_uuid_rejects_sql_injection(self) -> None:
        with pytest.raises(ValidationError):
            validate_uuid("'; DROP TABLE organisms; --")

    def test_uuid_rejects_script_injection(self) -> None:
        with pytest.raises(ValidationError):
            validate_uuid("<script>alert('xss')</script>")

    def test_string_rejects_null_bytes(self) -> None:
        with pytest.raises(ValidationError):
            validate_uuid("a1b2c3d4\x00-e5f6-7890-abcd-ef1234567890")

    def test_long_input_rejected(self) -> None:
        with pytest.raises(ValidationError):
            validate_string_not_empty("A" * 10000, "name", max_length=128)
