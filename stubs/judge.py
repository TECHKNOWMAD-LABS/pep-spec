"""PEP-002 Judge — evaluates organisms against criteria."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar


class Metric(str, Enum):
    ACCURACY = "accuracy"
    LATENCY = "latency"
    COST = "cost"
    SAFETY = "safety"
    CREATIVITY = "creativity"


@dataclass
class Criterion:
    name: str
    weight: float
    threshold: float
    metric: Metric

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Criterion:
        return cls(
            name=data["name"],
            weight=data["weight"],
            threshold=data["threshold"],
            metric=Metric(data["metric"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "weight": self.weight,
            "threshold": self.threshold,
            "metric": self.metric.value,
        }


@dataclass
class VerdictDetail:
    criterion: str
    score: float
    passed: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> VerdictDetail:
        return cls(criterion=data["criterion"], score=data["score"], passed=data["passed"])

    def to_dict(self) -> dict[str, Any]:
        return {"criterion": self.criterion, "score": self.score, "passed": self.passed}


@dataclass
class Verdict:
    organism_id: str
    score: float
    passed: bool
    details: list[VerdictDetail] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Verdict:
        return cls(
            organism_id=data["organism_id"],
            score=data["score"],
            passed=data["passed"],
            details=[VerdictDetail.from_dict(d) for d in data["details"]],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "organism_id": self.organism_id,
            "score": self.score,
            "passed": self.passed,
            "details": [d.to_dict() for d in self.details],
        }


@dataclass
class JudgeConfig:
    max_retries: int
    timeout_ms: int
    parallel: bool

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> JudgeConfig:
        return cls(
            max_retries=data["max_retries"],
            timeout_ms=data["timeout_ms"],
            parallel=data["parallel"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_retries": self.max_retries,
            "timeout_ms": self.timeout_ms,
            "parallel": self.parallel,
        }


@dataclass
class Judge:
    id: str
    name: str
    version: str
    criteria: list[Criterion]
    verdict: Verdict
    config: JudgeConfig

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Judge:
        return cls(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            criteria=[Criterion.from_dict(c) for c in data["criteria"]],
            verdict=Verdict.from_dict(data["verdict"]),
            config=JudgeConfig.from_dict(data["config"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "criteria": [c.to_dict() for c in self.criteria],
            "verdict": self.verdict.to_dict(),
            "config": self.config.to_dict(),
        }
