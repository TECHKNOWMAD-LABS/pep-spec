"""PEP-001 Organism conformance tests — 22 tests."""

from __future__ import annotations

import copy
from typing import Any

import jsonschema
import pytest

from conformance.helpers import VALID_DATETIME, VALID_UUID, VALID_UUID_2, load_schema
from stubs.organism import Constraint, Genome, Organism, OrganismStatus, Trait

SCHEMA = load_schema("organism")


# ── Schema validation: valid payloads ───────────────────────────────────────

def test_valid_organism_passes_schema(valid_organism: dict[str, Any]) -> None:
    jsonschema.validate(valid_organism, SCHEMA)


def test_minimal_organism_passes_schema() -> None:
    doc = {
        "id": VALID_UUID,
        "name": "x",
        "version": "0.0.1",
        "genome": {"traits": [], "mutations": []},
        "phenotype": {"capabilities": [], "constraints": []},
        "metadata": {"created_at": VALID_DATETIME, "updated_at": VALID_DATETIME, "tags": [], "lineage": []},
        "status": "embryo",
    }
    jsonschema.validate(doc, SCHEMA)


def test_organism_with_lineage() -> None:
    doc = {
        "id": VALID_UUID,
        "name": "child",
        "version": "1.0.0",
        "genome": {"traits": [], "mutations": []},
        "phenotype": {"capabilities": [], "constraints": []},
        "metadata": {"created_at": VALID_DATETIME, "updated_at": VALID_DATETIME, "tags": [], "lineage": [VALID_UUID_2]},
        "status": "alive",
    }
    jsonschema.validate(doc, SCHEMA)


def test_organism_all_statuses() -> None:
    for status in ["embryo", "alive", "dormant", "dead"]:
        doc = {
            "id": VALID_UUID, "name": "s", "version": "1.0.0",
            "genome": {"traits": [], "mutations": []},
            "phenotype": {"capabilities": [], "constraints": []},
            "metadata": {"created_at": VALID_DATETIME, "updated_at": VALID_DATETIME, "tags": [], "lineage": []},
            "status": status,
        }
        jsonschema.validate(doc, SCHEMA)


def test_organism_all_mutation_operations() -> None:
    for op in ["add", "remove", "modify"]:
        doc = {
            "id": VALID_UUID, "name": "m", "version": "1.0.0",
            "genome": {"traits": [], "mutations": [{"gene": "g", "operation": op, "payload": None}]},
            "phenotype": {"capabilities": [], "constraints": []},
            "metadata": {"created_at": VALID_DATETIME, "updated_at": VALID_DATETIME, "tags": [], "lineage": []},
            "status": "alive",
        }
        jsonschema.validate(doc, SCHEMA)


# ── Schema validation: invalid payloads ─────────────────────────────────────

def test_organism_missing_id(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    del doc["id"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_missing_name(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    del doc["name"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_empty_name(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    doc["name"] = ""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_name_too_long(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    doc["name"] = "x" * 129
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_invalid_semver(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    doc["version"] = "not-semver"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_invalid_uuid(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    doc["id"] = "not-a-uuid"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_invalid_status(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    doc["status"] = "zombie"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_trait_weight_out_of_range(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    doc["genome"]["traits"][0]["weight"] = 1.5
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_invalid_mutation_operation(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    doc["genome"]["mutations"][0]["operation"] = "delete"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_additional_properties(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    doc["extra_field"] = "not allowed"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_organism_negative_trait_weight(valid_organism: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_organism)
    doc["genome"]["traits"][0]["weight"] = -0.1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


# ── Python stub tests ───────────────────────────────────────────────────────

def test_organism_stub_from_dict(valid_organism: dict[str, Any]) -> None:
    org = Organism.from_dict(valid_organism)
    assert org.id == VALID_UUID
    assert org.name == "test-organism"
    assert org.status == OrganismStatus.ALIVE


def test_organism_stub_roundtrip(valid_organism: dict[str, Any]) -> None:
    org = Organism.from_dict(valid_organism)
    assert org.to_dict() == valid_organism


def test_organism_stub_trait() -> None:
    t = Trait(name="speed", value=10, weight=0.5)
    assert t.to_dict() == {"name": "speed", "value": 10, "weight": 0.5}


def test_organism_stub_genome_empty() -> None:
    g = Genome(traits=[], mutations=[])
    assert g.to_dict() == {"traits": [], "mutations": []}


def test_organism_stub_status_enum() -> None:
    assert OrganismStatus.EMBRYO.value == "embryo"
    assert OrganismStatus.DEAD.value == "dead"


def test_organism_stub_constraint() -> None:
    c = Constraint(resource="cpu", limit=4.0)
    rt = Constraint.from_dict(c.to_dict())
    assert rt.resource == "cpu"
    assert rt.limit == 4.0
