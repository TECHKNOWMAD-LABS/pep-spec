"""PEP-004 Event Log conformance tests — 18 tests."""

from __future__ import annotations

import copy
from typing import Any

import jsonschema
import pytest

from conformance.helpers import VALID_UUID, VALID_UUID_2, VALID_UUID_3, VALID_CHECKSUM, VALID_DATETIME, load_schema
from stubs.event_log import EventLog, EventSource, EventType, ComponentType

SCHEMA = load_schema("event-log")


# ── Schema: valid ───────────────────────────────────────────────────────────

def test_valid_event_log_passes_schema(valid_event_log: dict[str, Any]) -> None:
    jsonschema.validate(valid_event_log, SCHEMA)


def test_event_log_with_correlation_id(valid_event_log: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_event_log)
    doc["correlation_id"] = VALID_UUID_3
    jsonschema.validate(doc, SCHEMA)


def test_event_log_all_types() -> None:
    types = [
        "organism.created", "organism.mutated", "organism.evaluated", "organism.died",
        "generation.started", "generation.completed", "engine.started", "engine.stopped",
        "judge.verdict", "sharing.exported", "sharing.imported", "privacy.redacted", "agent.action",
    ]
    for t in types:
        doc = {
            "id": VALID_UUID, "timestamp": VALID_DATETIME, "type": t,
            "source": {"component": "engine", "id": VALID_UUID_2},
            "payload": {}, "sequence": 0, "checksum": VALID_CHECKSUM,
        }
        jsonschema.validate(doc, SCHEMA)


def test_event_log_all_components() -> None:
    for comp in ["organism", "judge", "engine", "sharing", "privacy", "agent"]:
        doc = {
            "id": VALID_UUID, "timestamp": VALID_DATETIME, "type": "organism.created",
            "source": {"component": comp, "id": VALID_UUID_2},
            "payload": {}, "sequence": 0, "checksum": VALID_CHECKSUM,
        }
        jsonschema.validate(doc, SCHEMA)


# ── Schema: invalid ─────────────────────────────────────────────────────────

def test_event_log_missing_type(valid_event_log: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_event_log)
    del doc["type"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_event_log_invalid_type(valid_event_log: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_event_log)
    doc["type"] = "organism.resurrected"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_event_log_invalid_component(valid_event_log: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_event_log)
    doc["source"]["component"] = "database"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_event_log_negative_sequence(valid_event_log: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_event_log)
    doc["sequence"] = -1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_event_log_invalid_checksum(valid_event_log: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_event_log)
    doc["checksum"] = "tooshort"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_event_log_invalid_correlation_id(valid_event_log: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_event_log)
    doc["correlation_id"] = "not-a-uuid"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_event_log_missing_checksum(valid_event_log: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_event_log)
    del doc["checksum"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_event_log_additional_properties(valid_event_log: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_event_log)
    doc["extra"] = 1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


# ── Stub tests ──────────────────────────────────────────────────────────────

def test_event_log_stub_from_dict(valid_event_log: dict[str, Any]) -> None:
    e = EventLog.from_dict(valid_event_log)
    assert e.type == EventType.ORGANISM_CREATED
    assert e.sequence == 0
    assert e.correlation_id is None


def test_event_log_stub_roundtrip(valid_event_log: dict[str, Any]) -> None:
    e = EventLog.from_dict(valid_event_log)
    assert e.to_dict() == valid_event_log


def test_event_log_stub_with_correlation() -> None:
    data = {
        "id": VALID_UUID, "timestamp": VALID_DATETIME, "type": "agent.action",
        "source": {"component": "agent", "id": VALID_UUID_2},
        "payload": {"action": "mutate"}, "sequence": 42,
        "correlation_id": VALID_UUID_3, "checksum": VALID_CHECKSUM,
    }
    e = EventLog.from_dict(data)
    assert e.correlation_id == VALID_UUID_3
    assert e.to_dict() == data


def test_event_log_event_type_enum() -> None:
    assert EventType.JUDGE_VERDICT.value == "judge.verdict"
    assert EventType.PRIVACY_REDACTED.value == "privacy.redacted"


def test_event_log_component_type_enum() -> None:
    assert ComponentType.ORGANISM.value == "organism"
    assert ComponentType.AGENT.value == "agent"


def test_event_log_source_roundtrip() -> None:
    src = EventSource(component=ComponentType.ENGINE, id=VALID_UUID)
    rt = EventSource.from_dict(src.to_dict())
    assert rt.component == ComponentType.ENGINE
