"""PEP-003 Engine conformance tests — 20 tests."""

from __future__ import annotations

import copy
from typing import Any

import jsonschema
import pytest

from conformance.helpers import VALID_UUID, VALID_UUID_2, VALID_UUID_3, load_schema
from stubs.engine import (
    Engine, Population, Selection, Crossover, EngineMutation, Termination,
    SelectionStrategy, CrossoverMethod,
)

SCHEMA = load_schema("engine")


# ── Schema: valid ───────────────────────────────────────────────────────────

def test_valid_engine_passes_schema(valid_engine: dict[str, Any]) -> None:
    jsonschema.validate(valid_engine, SCHEMA)


def test_engine_all_selection_strategies() -> None:
    for strat in ["tournament", "roulette", "rank", "elite"]:
        doc = {
            "id": VALID_UUID, "name": "e", "version": "1.0.0",
            "population": {"size": 1, "organisms": [], "generation": 0},
            "selection": {"strategy": strat, "pressure": 0.5, "elitism_rate": 0.1},
            "crossover": {"method": "uniform", "rate": 0.5},
            "mutation": {"rate": 0.1, "decay": 0.0},
            "termination": {"max_generations": 10, "fitness_target": 0.9, "stagnation_limit": 5},
        }
        jsonschema.validate(doc, SCHEMA)


def test_engine_all_crossover_methods() -> None:
    for method in ["single_point", "two_point", "uniform", "none"]:
        doc = {
            "id": VALID_UUID, "name": "e", "version": "1.0.0",
            "population": {"size": 1, "organisms": [], "generation": 0},
            "selection": {"strategy": "tournament", "pressure": 0.5, "elitism_rate": 0.1},
            "crossover": {"method": method, "rate": 0.5},
            "mutation": {"rate": 0.1, "decay": 0.0},
            "termination": {"max_generations": 10, "fitness_target": 0.9, "stagnation_limit": 5},
        }
        jsonschema.validate(doc, SCHEMA)


def test_engine_boundary_rates() -> None:
    doc = {
        "id": VALID_UUID, "name": "e", "version": "1.0.0",
        "population": {"size": 1, "organisms": [], "generation": 0},
        "selection": {"strategy": "tournament", "pressure": 0.0, "elitism_rate": 1.0},
        "crossover": {"method": "none", "rate": 0.0},
        "mutation": {"rate": 1.0, "decay": 0.0},
        "termination": {"max_generations": 1, "fitness_target": 0.0, "stagnation_limit": 1},
    }
    jsonschema.validate(doc, SCHEMA)


# ── Schema: invalid ─────────────────────────────────────────────────────────

def test_engine_missing_population(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    del doc["population"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_engine_zero_population_size(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    doc["population"]["size"] = 0
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_engine_negative_generation(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    doc["population"]["generation"] = -1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_engine_invalid_strategy(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    doc["selection"]["strategy"] = "random"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_engine_invalid_crossover_method(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    doc["crossover"]["method"] = "triple_point"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_engine_pressure_above_one(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    doc["selection"]["pressure"] = 1.1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_engine_mutation_rate_negative(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    doc["mutation"]["rate"] = -0.01
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_engine_zero_max_generations(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    doc["termination"]["max_generations"] = 0
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_engine_additional_properties(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    doc["extra"] = "nope"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_engine_invalid_organism_uuid(valid_engine: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_engine)
    doc["population"]["organisms"] = ["not-uuid"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


# ── Stub tests ──────────────────────────────────────────────────────────────

def test_engine_stub_from_dict(valid_engine: dict[str, Any]) -> None:
    e = Engine.from_dict(valid_engine)
    assert e.name == "main-engine"
    assert e.population.size == 100


def test_engine_stub_roundtrip(valid_engine: dict[str, Any]) -> None:
    e = Engine.from_dict(valid_engine)
    assert e.to_dict() == valid_engine


def test_engine_selection_strategy_enum() -> None:
    assert SelectionStrategy.TOURNAMENT.value == "tournament"
    assert SelectionStrategy.ELITE.value == "elite"


def test_engine_crossover_method_enum() -> None:
    assert CrossoverMethod.SINGLE_POINT.value == "single_point"
    assert CrossoverMethod.NONE.value == "none"


def test_engine_population_roundtrip() -> None:
    p = Population(size=10, organisms=[VALID_UUID], generation=5)
    rt = Population.from_dict(p.to_dict())
    assert rt.size == 10
    assert rt.generation == 5


def test_engine_termination_roundtrip() -> None:
    t = Termination(max_generations=100, fitness_target=0.99, stagnation_limit=20)
    rt = Termination.from_dict(t.to_dict())
    assert rt.fitness_target == 0.99
