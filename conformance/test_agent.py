"""PEP-007 Agent conformance tests — 13 tests."""

from __future__ import annotations

import copy
from typing import Any

import jsonschema
import pytest

from conformance.helpers import VALID_UUID, VALID_UUID_2, load_schema
from stubs.agent import Agent, AgentBindings, AgentRole, AgentState, AgentStatus

SCHEMA = load_schema("agent")


# ── Schema: valid ───────────────────────────────────────────────────────────

def test_valid_agent_passes_schema(valid_agent: dict[str, Any]) -> None:
    jsonschema.validate(valid_agent, SCHEMA)


def test_agent_all_roles() -> None:
    for role in ["evolver", "guardian", "explorer", "harvester", "orchestrator"]:
        doc = {
            "id": VALID_UUID, "name": "a", "version": "1.0.0", "role": role,
            "capabilities": [],
            "bindings": {"organism_ids": [], "judge_ids": []},
            "policy": {
                "max_actions_per_minute": 1, "require_approval": False,
                "allowed_actions": [], "denied_actions": [],
            },
            "state": {"status": "idle", "error_count": 0},
        }
        jsonschema.validate(doc, SCHEMA)


def test_agent_all_statuses() -> None:
    for status in ["idle", "active", "suspended", "terminated"]:
        doc = {
            "id": VALID_UUID, "name": "a", "version": "1.0.0", "role": "guardian",
            "capabilities": [],
            "bindings": {"organism_ids": [], "judge_ids": []},
            "policy": {
                "max_actions_per_minute": 1, "require_approval": False,
                "allowed_actions": [], "denied_actions": [],
            },
            "state": {"status": status, "error_count": 0},
        }
        jsonschema.validate(doc, SCHEMA)


# ── Schema: invalid ─────────────────────────────────────────────────────────

def test_agent_invalid_role(valid_agent: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_agent)
    doc["role"] = "destroyer"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_agent_invalid_status(valid_agent: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_agent)
    doc["state"]["status"] = "crashed"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_agent_zero_max_actions(valid_agent: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_agent)
    doc["policy"]["max_actions_per_minute"] = 0
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_agent_negative_error_count(valid_agent: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_agent)
    doc["state"]["error_count"] = -1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_agent_additional_properties(valid_agent: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_agent)
    doc["extra"] = "nope"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


# ── Stub tests ──────────────────────────────────────────────────────────────

def test_agent_stub_from_dict(valid_agent: dict[str, Any]) -> None:
    a = Agent.from_dict(valid_agent)
    assert a.role == AgentRole.EVOLVER
    assert a.state.status == AgentStatus.ACTIVE
    assert a.bindings.engine_id == VALID_UUID_2


def test_agent_stub_roundtrip(valid_agent: dict[str, Any]) -> None:
    a = Agent.from_dict(valid_agent)
    assert a.to_dict() == valid_agent


def test_agent_state_minimal() -> None:
    s = AgentState(status=AgentStatus.IDLE, error_count=0)
    d = s.to_dict()
    assert "current_task" not in d
    assert "last_action_at" not in d


def test_agent_bindings_without_engine() -> None:
    b = AgentBindings(organism_ids=[VALID_UUID], judge_ids=[])
    d = b.to_dict()
    assert "engine_id" not in d


def test_agent_role_enum() -> None:
    assert AgentRole.ORCHESTRATOR.value == "orchestrator"
    assert AgentStatus.TERMINATED.value == "terminated"
