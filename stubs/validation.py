"""PEP validation utilities — input validation for from_dict deserialization."""

from __future__ import annotations

import re
from typing import Any

UUID_RE = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
SEMVER_RE = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)
ISO8601_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}")


class ValidationError(Exception):
    """Raised when input data fails validation."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")


def require_field(data: dict[str, Any], field: str, expected_type: type | None = None) -> Any:
    """Ensure a required field exists and optionally check its type."""
    if not isinstance(data, dict):
        raise ValidationError(field, f"expected dict, got {type(data).__name__}")
    if field not in data:
        raise ValidationError(field, "required field is missing")
    value = data[field]
    if expected_type is not None and not isinstance(value, expected_type):
        raise ValidationError(field, f"expected {expected_type.__name__}, got {type(value).__name__}")
    return value


def validate_uuid(value: str, field: str = "id") -> str:
    """Validate a UUID string."""
    if not isinstance(value, str):
        raise ValidationError(field, f"expected string, got {type(value).__name__}")
    if not UUID_RE.match(value):
        raise ValidationError(field, f"invalid UUID format: {value!r}")
    return value


def validate_semver(value: str, field: str = "version") -> str:
    """Validate a semantic version string."""
    if not isinstance(value, str):
        raise ValidationError(field, f"expected string, got {type(value).__name__}")
    if not SEMVER_RE.match(value):
        raise ValidationError(field, f"invalid semver format: {value!r}")
    return value


def validate_range(value: float | int, field: str, min_val: float | None = None, max_val: float | None = None) -> float | int:
    """Validate a numeric value is within range."""
    if not isinstance(value, (int, float)):
        raise ValidationError(field, f"expected number, got {type(value).__name__}")
    if min_val is not None and value < min_val:
        raise ValidationError(field, f"value {value} is below minimum {min_val}")
    if max_val is not None and value > max_val:
        raise ValidationError(field, f"value {value} exceeds maximum {max_val}")
    return value


def validate_enum_value(value: str, valid_values: set[str], field: str) -> str:
    """Validate a string is one of the allowed enum values."""
    if not isinstance(value, str):
        raise ValidationError(field, f"expected string, got {type(value).__name__}")
    if value not in valid_values:
        raise ValidationError(field, f"invalid value {value!r}, expected one of {sorted(valid_values)}")
    return value


def validate_string_not_empty(value: str, field: str, max_length: int | None = None) -> str:
    """Validate a string is non-empty and optionally within max length."""
    if not isinstance(value, str):
        raise ValidationError(field, f"expected string, got {type(value).__name__}")
    if not value:
        raise ValidationError(field, "string must not be empty")
    if max_length is not None and len(value) > max_length:
        raise ValidationError(field, f"string length {len(value)} exceeds maximum {max_length}")
    return value


def validate_list(value: Any, field: str, min_length: int = 0) -> list:
    """Validate a value is a list with minimum length."""
    if not isinstance(value, list):
        raise ValidationError(field, f"expected list, got {type(value).__name__}")
    if len(value) < min_length:
        raise ValidationError(field, f"list must have at least {min_length} items, got {len(value)}")
    return value
