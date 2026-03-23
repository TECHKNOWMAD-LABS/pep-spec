"""PEP-002 Judge conformance tests — 18 tests."""

from __future__ import annotations

import copy
from typing import Any

import jsonschema
import pytest

from conformance.helpers import VALID_UUID, VALID_UUID_2, load_schema
from stubs.judge import Criterion, Judge, JudgeConfig, Metric, VerdictDetail

SCHEMA = load_schema("judge")


# ── Schema: valid ───────────────────────────────────────────────────────────

def test_valid_judge_passes_schema(valid_judge: dict[str, Any]) -> None:
    jsonschema.validate(valid_judge, SCHEMA)


def test_judge_all_metrics() -> None:
    for metric in ["accuracy", "latency", "cost", "safety", "creativity"]:
        doc = {
            "id": VALID_UUID, "name": "j", "version": "1.0.0",
            "criteria": [{"name": "c", "weight": 0.5, "threshold": 0.5, "metric": metric}],
            "verdict": {"organism_id": VALID_UUID_2, "score": 0.5, "passed": True, "details": []},
            "config": {"max_retries": 0, "timeout_ms": 1, "parallel": False},
        }
        jsonschema.validate(doc, SCHEMA)


# ── Schema: invalid ─────────────────────────────────────────────────────────

def test_judge_missing_criteria(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    del doc["criteria"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_judge_empty_criteria(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    doc["criteria"] = []
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_judge_invalid_metric(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    doc["criteria"][0]["metric"] = "fun"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_judge_weight_above_one(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    doc["criteria"][0]["weight"] = 1.1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_judge_negative_retries(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    doc["config"]["max_retries"] = -1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_judge_zero_timeout(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    doc["config"]["timeout_ms"] = 0
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_judge_verdict_invalid_organism_id(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    doc["verdict"]["organism_id"] = "bad"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_judge_score_above_one(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    doc["verdict"]["score"] = 1.5
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_judge_additional_properties(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    doc["extra"] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_judge_missing_verdict(valid_judge: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_judge)
    del doc["verdict"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


# ── Stub tests ──────────────────────────────────────────────────────────────

def test_judge_stub_from_dict(valid_judge: dict[str, Any]) -> None:
    j = Judge.from_dict(valid_judge)
    assert j.name == "accuracy-judge"
    assert len(j.criteria) == 2
    assert j.verdict.passed is True


def test_judge_stub_roundtrip(valid_judge: dict[str, Any]) -> None:
    j = Judge.from_dict(valid_judge)
    assert j.to_dict() == valid_judge


def test_judge_criterion_metric_enum() -> None:
    c = Criterion(name="c", weight=0.5, threshold=0.5, metric=Metric.SAFETY)
    assert c.metric.value == "safety"


def test_judge_verdict_detail() -> None:
    d = VerdictDetail(criterion="acc", score=0.9, passed=True)
    rt = VerdictDetail.from_dict(d.to_dict())
    assert rt.criterion == "acc"


def test_judge_config_roundtrip() -> None:
    cfg = JudgeConfig(max_retries=5, timeout_ms=3000, parallel=False)
    rt = JudgeConfig.from_dict(cfg.to_dict())
    assert rt.max_retries == 5
    assert rt.parallel is False


def test_judge_stub_verdict_organism_id(valid_judge: dict[str, Any]) -> None:
    j = Judge.from_dict(valid_judge)
    assert j.verdict.organism_id == VALID_UUID_2
