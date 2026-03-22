"""Shared fixtures for PEP conformance tests."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

# Ensure project root is on sys.path so stubs can be imported.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from conformance.helpers import VALID_UUID, VALID_UUID_2, VALID_UUID_3, VALID_CHECKSUM, VALID_DATETIME


# ── Valid fixture payloads ──────────────────────────────────────────────────

@pytest.fixture
def valid_organism() -> dict[str, Any]:
    return {
        "id": VALID_UUID,
        "name": "test-organism",
        "version": "1.0.0",
        "genome": {
            "traits": [{"name": "speed", "value": 42, "weight": 0.8}],
            "mutations": [{"gene": "speed", "operation": "modify", "payload": {"delta": 5}}],
        },
        "phenotype": {
            "capabilities": ["run", "jump"],
            "constraints": [{"resource": "memory", "limit": 1024}],
        },
        "metadata": {
            "created_at": VALID_DATETIME,
            "updated_at": VALID_DATETIME,
            "tags": ["fast", "v1"],
            "lineage": [],
        },
        "status": "alive",
    }


@pytest.fixture
def valid_judge() -> dict[str, Any]:
    return {
        "id": VALID_UUID,
        "name": "accuracy-judge",
        "version": "1.0.0",
        "criteria": [
            {"name": "accuracy", "weight": 0.7, "threshold": 0.9, "metric": "accuracy"},
            {"name": "speed", "weight": 0.3, "threshold": 0.5, "metric": "latency"},
        ],
        "verdict": {
            "organism_id": VALID_UUID_2,
            "score": 0.85,
            "passed": True,
            "details": [
                {"criterion": "accuracy", "score": 0.92, "passed": True},
                {"criterion": "speed", "score": 0.75, "passed": True},
            ],
        },
        "config": {"max_retries": 3, "timeout_ms": 5000, "parallel": True},
    }


@pytest.fixture
def valid_engine() -> dict[str, Any]:
    return {
        "id": VALID_UUID,
        "name": "main-engine",
        "version": "2.1.0",
        "population": {
            "size": 100,
            "organisms": [VALID_UUID_2, VALID_UUID_3],
            "generation": 0,
        },
        "selection": {"strategy": "tournament", "pressure": 0.7, "elitism_rate": 0.1},
        "crossover": {"method": "single_point", "rate": 0.8},
        "mutation": {"rate": 0.05, "decay": 0.01},
        "termination": {"max_generations": 500, "fitness_target": 0.95, "stagnation_limit": 50},
    }


@pytest.fixture
def valid_event_log() -> dict[str, Any]:
    return {
        "id": VALID_UUID,
        "timestamp": VALID_DATETIME,
        "type": "organism.created",
        "source": {"component": "engine", "id": VALID_UUID_2},
        "payload": {"organism_id": VALID_UUID_3},
        "sequence": 0,
        "checksum": VALID_CHECKSUM,
    }


@pytest.fixture
def valid_sharing() -> dict[str, Any]:
    return {
        "id": VALID_UUID,
        "format": "pep-native",
        "source": {
            "organism_id": VALID_UUID_2,
            "engine_id": VALID_UUID_3,
            "generation": 42,
        },
        "target": {"uri": "https://example.com/export/42", "protocol": "https"},
        "content": {"genome": True, "phenotype": True, "history": False, "size_bytes": 102400},
        "integrity": {
            "algorithm": "sha256",
            "hash": VALID_CHECKSUM,
        },
        "permissions": {
            "public": False,
            "allowed_consumers": [VALID_UUID],
        },
    }


@pytest.fixture
def valid_privacy() -> dict[str, Any]:
    return {
        "id": VALID_UUID,
        "version": "1.0.0",
        "scope": "organism",
        "rules": [
            {"field": "genome.traits", "action": "redact", "condition": {"context": "export"}},
            {"field": "metadata.tags", "action": "omit"},
        ],
        "retention": {"max_age_days": 365, "auto_purge": True},
        "consent": {"required": True, "granted_by": VALID_UUID_2, "granted_at": VALID_DATETIME},
        "audit": {"log_access": True, "log_mutations": True, "require_justification": False},
    }


@pytest.fixture
def valid_agent() -> dict[str, Any]:
    return {
        "id": VALID_UUID,
        "name": "evolver-alpha",
        "version": "1.0.0",
        "role": "evolver",
        "capabilities": ["mutate", "crossover", "select"],
        "bindings": {
            "engine_id": VALID_UUID_2,
            "organism_ids": [VALID_UUID_3],
            "judge_ids": [],
        },
        "policy": {
            "max_actions_per_minute": 60,
            "require_approval": False,
            "allowed_actions": ["mutate", "crossover"],
            "denied_actions": ["terminate"],
        },
        "state": {
            "status": "active",
            "current_task": "mutating generation 42",
            "last_action_at": VALID_DATETIME,
            "error_count": 0,
        },
    }
