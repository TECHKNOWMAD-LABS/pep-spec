"""PEP-006 Privacy — data protection rules."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from stubs.validation import (
    require_field,
    validate_enum_value,
    validate_range,
    validate_semver,
    validate_uuid,
)


class PrivacyScope(str, Enum):
    """Scopes for privacy policies: organism, judge, engine, event, global."""

    ORGANISM = "organism"
    JUDGE = "judge"
    ENGINE = "engine"
    EVENT = "event"
    GLOBAL = "global"


class RuleAction(str, Enum):
    """Privacy actions: redact, hash, encrypt, omit, generalize."""

    REDACT = "redact"
    HASH = "hash"
    ENCRYPT = "encrypt"
    OMIT = "omit"
    GENERALIZE = "generalize"


class ConditionContext(str, Enum):
    """Contexts when privacy rules apply: export, log, api, always."""

    EXPORT = "export"
    LOG = "log"
    API = "api"
    ALWAYS = "always"


@dataclass
class RuleCondition:
    context: ConditionContext

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> RuleCondition:
        return cls(context=ConditionContext(data["context"]))

    def to_dict(self) -> dict[str, Any]:
        return {"context": self.context.value}


@dataclass
class PrivacyRule:
    field: str
    action: RuleAction
    condition: RuleCondition | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PrivacyRule:
        return cls(
            field=data["field"],
            action=RuleAction(data["action"]),
            condition=(
                RuleCondition.from_dict(data["condition"])
                if "condition" in data and data["condition"] is not None
                else None
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"field": self.field, "action": self.action.value}
        if self.condition is not None:
            result["condition"] = self.condition.to_dict()
        return result


@dataclass
class Retention:
    max_age_days: int
    auto_purge: bool
    archive_after_days: int | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Retention:
        validate_range(require_field(data, "max_age_days", int), "max_age_days", min_val=1)
        require_field(data, "auto_purge", bool)
        return cls(
            max_age_days=data["max_age_days"],
            auto_purge=data["auto_purge"],
            archive_after_days=data.get("archive_after_days"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "max_age_days": self.max_age_days,
            "auto_purge": self.auto_purge,
        }
        if self.archive_after_days is not None:
            result["archive_after_days"] = self.archive_after_days
        return result


@dataclass
class Consent:
    required: bool
    granted_by: str | None = None
    granted_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Consent:
        return cls(
            required=data["required"],
            granted_by=data.get("granted_by"),
            granted_at=data.get("granted_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {"required": self.required}
        if self.granted_by is not None:
            result["granted_by"] = self.granted_by
        if self.granted_at is not None:
            result["granted_at"] = self.granted_at
        return result


@dataclass
class Audit:
    log_access: bool
    log_mutations: bool
    require_justification: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Audit:
        return cls(
            log_access=data["log_access"],
            log_mutations=data["log_mutations"],
            require_justification=data["require_justification"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "log_access": self.log_access,
            "log_mutations": self.log_mutations,
            "require_justification": self.require_justification,
        }


@dataclass
class PrivacyPolicy:
    id: str
    version: str
    scope: PrivacyScope
    rules: list[PrivacyRule] = field(default_factory=list)
    retention: Retention = field(default_factory=lambda: Retention(max_age_days=365, auto_purge=False))
    consent: Consent = field(default_factory=lambda: Consent(required=False))
    audit: Audit = field(
        default_factory=lambda: Audit(log_access=True, log_mutations=True, require_justification=False),
    )

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PrivacyPolicy:
        validate_uuid(require_field(data, "id", str), "id")
        validate_semver(require_field(data, "version", str), "version")
        validate_enum_value(require_field(data, "scope", str), {s.value for s in PrivacyScope}, "scope")
        return cls(
            id=data["id"],
            version=data["version"],
            scope=PrivacyScope(data["scope"]),
            rules=[PrivacyRule.from_dict(r) for r in data["rules"]],
            retention=Retention.from_dict(data["retention"]),
            consent=Consent.from_dict(data["consent"]),
            audit=Audit.from_dict(data["audit"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "version": self.version,
            "scope": self.scope.value,
            "rules": [r.to_dict() for r in self.rules],
            "retention": self.retention.to_dict(),
            "consent": self.consent.to_dict(),
            "audit": self.audit.to_dict(),
        }
