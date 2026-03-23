"""PEP-004 Event Log — immutable event records."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any

from stubs.validation import (
    require_field,
    validate_enum_value,
    validate_range,
    validate_string_not_empty,
    validate_uuid,
)


class EventType(str, Enum):
    ORGANISM_CREATED = "organism.created"
    ORGANISM_MUTATED = "organism.mutated"
    ORGANISM_EVALUATED = "organism.evaluated"
    ORGANISM_DIED = "organism.died"
    GENERATION_STARTED = "generation.started"
    GENERATION_COMPLETED = "generation.completed"
    ENGINE_STARTED = "engine.started"
    ENGINE_STOPPED = "engine.stopped"
    JUDGE_VERDICT = "judge.verdict"
    SHARING_EXPORTED = "sharing.exported"
    SHARING_IMPORTED = "sharing.imported"
    PRIVACY_REDACTED = "privacy.redacted"
    AGENT_ACTION = "agent.action"


class ComponentType(str, Enum):
    ORGANISM = "organism"
    JUDGE = "judge"
    ENGINE = "engine"
    SHARING = "sharing"
    PRIVACY = "privacy"
    AGENT = "agent"


@dataclass
class EventSource:
    component: ComponentType
    id: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EventSource:
        return cls(component=ComponentType(data["component"]), id=data["id"])

    def to_dict(self) -> dict[str, Any]:
        return {"component": self.component.value, "id": self.id}


@dataclass
class EventLog:
    id: str
    timestamp: str
    type: EventType
    source: EventSource
    payload: dict[str, Any]
    sequence: int
    checksum: str
    correlation_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EventLog:
        validate_uuid(require_field(data, "id", str), "id")
        require_field(data, "timestamp", str)
        validate_enum_value(require_field(data, "type", str), {e.value for e in EventType}, "type")
        require_field(data, "source", dict)
        validate_range(require_field(data, "sequence", int), "sequence", min_val=0)
        validate_string_not_empty(require_field(data, "checksum", str), "checksum")
        correlation_id = data.get("correlation_id")
        if correlation_id is not None:
            validate_uuid(correlation_id, "correlation_id")
        return cls(
            id=data["id"],
            timestamp=data["timestamp"],
            type=EventType(data["type"]),
            source=EventSource.from_dict(data["source"]),
            payload=data["payload"],
            sequence=data["sequence"],
            checksum=data["checksum"],
            correlation_id=correlation_id,
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "id": self.id,
            "timestamp": self.timestamp,
            "type": self.type.value,
            "source": self.source.to_dict(),
            "payload": self.payload,
            "sequence": self.sequence,
            "checksum": self.checksum,
        }
        if self.correlation_id is not None:
            result["correlation_id"] = self.correlation_id
        return result
