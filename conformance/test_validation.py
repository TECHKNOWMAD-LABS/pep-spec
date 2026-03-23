"""Tests for input validation — error hardening across all stubs."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from conformance.helpers import VALID_UUID, VALID_UUID_2, VALID_CHECKSUM, VALID_DATETIME

from stubs.validation import (
    ValidationError, require_field, validate_uuid, validate_semver,
    validate_range, validate_enum_value, validate_string_not_empty, validate_list,
)
from stubs.organism import Organism, Trait, Mutation
from stubs.judge import Judge, Criterion, Verdict
from stubs.engine import Engine, Population, Selection
from stubs.event_log import EventLog
from stubs.sharing import SharingManifest, SharingSource
from stubs.privacy import PrivacyPolicy, Retention
from stubs.agent import Agent, AgentPolicy


# ── Validation utility tests ─────────────────────────────────────────────


class TestRequireField:
    def test_missing_field_raises(self) -> None:
        with pytest.raises(ValidationError, match="required field is missing"):
            require_field({}, "name")

    def test_wrong_type_raises(self) -> None:
        with pytest.raises(ValidationError, match="expected str"):
            require_field({"name": 123}, "name", str)

    def test_not_a_dict_raises(self) -> None:
        with pytest.raises(ValidationError, match="expected dict"):
            require_field("not a dict", "field")

    def test_valid_field_returns_value(self) -> None:
        assert require_field({"x": 42}, "x", int) == 42


class TestValidateUuid:
    def test_valid_uuid(self) -> None:
        assert validate_uuid(VALID_UUID) == VALID_UUID

    def test_invalid_uuid(self) -> None:
        with pytest.raises(ValidationError, match="invalid UUID"):
            validate_uuid("not-a-uuid")

    def test_non_string_uuid(self) -> None:
        with pytest.raises(ValidationError, match="expected string"):
            validate_uuid(123)


class TestValidateSemver:
    def test_valid_semver(self) -> None:
        assert validate_semver("1.0.0") == "1.0.0"

    def test_valid_semver_prerelease(self) -> None:
        assert validate_semver("1.0.0-alpha.1") == "1.0.0-alpha.1"

    def test_invalid_semver(self) -> None:
        with pytest.raises(ValidationError, match="invalid semver"):
            validate_semver("not-semver")

    def test_non_string_semver(self) -> None:
        with pytest.raises(ValidationError, match="expected string"):
            validate_semver(100)


class TestValidateRange:
    def test_in_range(self) -> None:
        assert validate_range(0.5, "x", 0.0, 1.0) == 0.5

    def test_below_min(self) -> None:
        with pytest.raises(ValidationError, match="below minimum"):
            validate_range(-1, "x", min_val=0)

    def test_above_max(self) -> None:
        with pytest.raises(ValidationError, match="exceeds maximum"):
            validate_range(2.0, "x", max_val=1.0)

    def test_non_number(self) -> None:
        with pytest.raises(ValidationError, match="expected number"):
            validate_range("abc", "x", 0, 1)


class TestValidateEnumValue:
    def test_valid_value(self) -> None:
        assert validate_enum_value("a", {"a", "b"}, "x") == "a"

    def test_invalid_value(self) -> None:
        with pytest.raises(ValidationError, match="invalid value"):
            validate_enum_value("c", {"a", "b"}, "x")

    def test_non_string(self) -> None:
        with pytest.raises(ValidationError, match="expected string"):
            validate_enum_value(1, {"a"}, "x")


class TestValidateStringNotEmpty:
    def test_valid_string(self) -> None:
        assert validate_string_not_empty("hello", "x") == "hello"

    def test_empty_string(self) -> None:
        with pytest.raises(ValidationError, match="must not be empty"):
            validate_string_not_empty("", "x")

    def test_too_long(self) -> None:
        with pytest.raises(ValidationError, match="exceeds maximum"):
            validate_string_not_empty("a" * 200, "x", max_length=128)


class TestValidateList:
    def test_valid_list(self) -> None:
        assert validate_list([1, 2], "x") == [1, 2]

    def test_not_a_list(self) -> None:
        with pytest.raises(ValidationError, match="expected list"):
            validate_list("not list", "x")

    def test_too_short(self) -> None:
        with pytest.raises(ValidationError, match="at least 1"):
            validate_list([], "x", min_length=1)


# ── Stub validation integration tests ────────────────────────────────────


class TestOrganismValidation:
    def test_none_input(self) -> None:
        with pytest.raises(ValidationError):
            Organism.from_dict(None)

    def test_missing_id(self, valid_organism: dict) -> None:
        del valid_organism["id"]
        with pytest.raises(ValidationError, match="id.*missing"):
            Organism.from_dict(valid_organism)

    def test_invalid_uuid(self, valid_organism: dict) -> None:
        valid_organism["id"] = "bad-uuid"
        with pytest.raises(ValidationError, match="invalid UUID"):
            Organism.from_dict(valid_organism)

    def test_invalid_semver(self, valid_organism: dict) -> None:
        valid_organism["version"] = "nope"
        with pytest.raises(ValidationError, match="invalid semver"):
            Organism.from_dict(valid_organism)

    def test_name_too_long(self, valid_organism: dict) -> None:
        valid_organism["name"] = "x" * 200
        with pytest.raises(ValidationError, match="exceeds maximum"):
            Organism.from_dict(valid_organism)

    def test_empty_name(self, valid_organism: dict) -> None:
        valid_organism["name"] = ""
        with pytest.raises(ValidationError, match="must not be empty"):
            Organism.from_dict(valid_organism)

    def test_invalid_status(self, valid_organism: dict) -> None:
        valid_organism["status"] = "invalid"
        with pytest.raises(ValidationError, match="invalid value"):
            Organism.from_dict(valid_organism)


class TestTraitValidation:
    def test_weight_above_one(self) -> None:
        with pytest.raises(ValidationError, match="exceeds maximum"):
            Trait.from_dict({"name": "x", "value": 1, "weight": 1.5})

    def test_weight_below_zero(self) -> None:
        with pytest.raises(ValidationError, match="below minimum"):
            Trait.from_dict({"name": "x", "value": 1, "weight": -0.1})

    def test_missing_name(self) -> None:
        with pytest.raises(ValidationError, match="name.*missing"):
            Trait.from_dict({"value": 1, "weight": 0.5})


class TestMutationValidation:
    def test_invalid_operation(self) -> None:
        with pytest.raises(ValidationError, match="invalid value"):
            Mutation.from_dict({"gene": "x", "operation": "delete", "payload": None})


class TestJudgeValidation:
    def test_empty_criteria(self, valid_judge: dict) -> None:
        valid_judge["criteria"] = []
        with pytest.raises(ValidationError, match="at least 1"):
            Judge.from_dict(valid_judge)

    def test_invalid_verdict_score(self, valid_judge: dict) -> None:
        valid_judge["verdict"]["score"] = 2.0
        with pytest.raises(ValidationError, match="exceeds maximum"):
            Judge.from_dict(valid_judge)

    def test_criterion_weight_out_of_range(self) -> None:
        with pytest.raises(ValidationError, match="exceeds maximum"):
            Criterion.from_dict({"name": "x", "weight": 1.5, "threshold": 0.5, "metric": "accuracy"})


class TestEngineValidation:
    def test_zero_population_size(self, valid_engine: dict) -> None:
        valid_engine["population"]["size"] = 0
        with pytest.raises(ValidationError, match="below minimum"):
            Engine.from_dict(valid_engine)

    def test_pressure_out_of_range(self, valid_engine: dict) -> None:
        valid_engine["selection"]["pressure"] = 1.5
        with pytest.raises(ValidationError, match="exceeds maximum"):
            Engine.from_dict(valid_engine)


class TestEventLogValidation:
    def test_negative_sequence(self, valid_event_log: dict) -> None:
        valid_event_log["sequence"] = -1
        with pytest.raises(ValidationError, match="below minimum"):
            EventLog.from_dict(valid_event_log)

    def test_empty_checksum(self, valid_event_log: dict) -> None:
        valid_event_log["checksum"] = ""
        with pytest.raises(ValidationError, match="must not be empty"):
            EventLog.from_dict(valid_event_log)

    def test_invalid_correlation_id(self, valid_event_log: dict) -> None:
        valid_event_log["correlation_id"] = "not-a-uuid"
        with pytest.raises(ValidationError, match="invalid UUID"):
            EventLog.from_dict(valid_event_log)


class TestSharingValidation:
    def test_negative_generation(self) -> None:
        with pytest.raises(ValidationError, match="below minimum"):
            SharingSource.from_dict({
                "organism_id": VALID_UUID, "engine_id": VALID_UUID_2, "generation": -1
            })


class TestPrivacyValidation:
    def test_zero_max_age_days(self) -> None:
        with pytest.raises(ValidationError, match="below minimum"):
            Retention.from_dict({"max_age_days": 0, "auto_purge": True})


class TestAgentValidation:
    def test_zero_actions_per_minute(self) -> None:
        with pytest.raises(ValidationError, match="below minimum"):
            AgentPolicy.from_dict({
                "max_actions_per_minute": 0, "require_approval": False,
                "allowed_actions": [], "denied_actions": [],
            })

    def test_invalid_role(self, valid_agent: dict) -> None:
        valid_agent["role"] = "invalid"
        with pytest.raises(ValidationError, match="invalid value"):
            Agent.from_dict(valid_agent)
