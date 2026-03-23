"""PEP-006 Privacy conformance tests — 16 tests."""

from __future__ import annotations

import copy
from typing import Any

import jsonschema
import pytest

from conformance.helpers import VALID_UUID, load_schema
from stubs.privacy import (
    ConditionContext,
    Consent,
    PrivacyPolicy,
    PrivacyRule,
    PrivacyScope,
    Retention,
    RuleAction,
)

SCHEMA = load_schema("privacy")


# ── Schema: valid ───────────────────────────────────────────────────────────

def test_valid_privacy_passes_schema(valid_privacy: dict[str, Any]) -> None:
    jsonschema.validate(valid_privacy, SCHEMA)


def test_privacy_all_scopes() -> None:
    for scope in ["organism", "judge", "engine", "event", "global"]:
        doc = {
            "id": VALID_UUID, "version": "1.0.0", "scope": scope,
            "rules": [], "retention": {"max_age_days": 30, "auto_purge": False},
            "consent": {"required": False},
            "audit": {"log_access": False, "log_mutations": False, "require_justification": False},
        }
        jsonschema.validate(doc, SCHEMA)


def test_privacy_all_actions() -> None:
    for action in ["redact", "hash", "encrypt", "omit", "generalize"]:
        doc = {
            "id": VALID_UUID, "version": "1.0.0", "scope": "global",
            "rules": [{"field": "x", "action": action}],
            "retention": {"max_age_days": 1, "auto_purge": True},
            "consent": {"required": False},
            "audit": {"log_access": True, "log_mutations": True, "require_justification": True},
        }
        jsonschema.validate(doc, SCHEMA)


def test_privacy_with_archive(valid_privacy: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_privacy)
    doc["retention"]["archive_after_days"] = 90
    jsonschema.validate(doc, SCHEMA)


# ── Schema: invalid ─────────────────────────────────────────────────────────

def test_privacy_invalid_scope(valid_privacy: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_privacy)
    doc["scope"] = "network"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_privacy_invalid_action(valid_privacy: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_privacy)
    doc["rules"][0]["action"] = "delete"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_privacy_zero_max_age(valid_privacy: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_privacy)
    doc["retention"]["max_age_days"] = 0
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_privacy_invalid_condition_context(valid_privacy: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_privacy)
    doc["rules"][0]["condition"] = {"context": "internal"}
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_privacy_missing_retention(valid_privacy: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_privacy)
    del doc["retention"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_privacy_additional_properties(valid_privacy: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_privacy)
    doc["extra"] = "no"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


# ── Stub tests ──────────────────────────────────────────────────────────────

def test_privacy_stub_from_dict(valid_privacy: dict[str, Any]) -> None:
    p = PrivacyPolicy.from_dict(valid_privacy)
    assert p.scope == PrivacyScope.ORGANISM
    assert len(p.rules) == 2
    assert p.consent.required is True


def test_privacy_stub_roundtrip(valid_privacy: dict[str, Any]) -> None:
    p = PrivacyPolicy.from_dict(valid_privacy)
    assert p.to_dict() == valid_privacy


def test_privacy_rule_without_condition() -> None:
    r = PrivacyRule(field="x.y", action=RuleAction.HASH)
    d = r.to_dict()
    assert "condition" not in d
    rt = PrivacyRule.from_dict(d)
    assert rt.condition is None


def test_privacy_retention_without_archive() -> None:
    r = Retention(max_age_days=90, auto_purge=True)
    d = r.to_dict()
    assert "archive_after_days" not in d


def test_privacy_consent_minimal() -> None:
    c = Consent(required=False)
    d = c.to_dict()
    assert "granted_by" not in d
    assert "granted_at" not in d


def test_privacy_scope_enum() -> None:
    assert PrivacyScope.GLOBAL.value == "global"
    assert ConditionContext.ALWAYS.value == "always"
