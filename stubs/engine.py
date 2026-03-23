"""PEP-003 Engine — orchestrates the evolutionary process."""

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


class SelectionStrategy(str, Enum):
    TOURNAMENT = "tournament"
    ROULETTE = "roulette"
    RANK = "rank"
    ELITE = "elite"


class CrossoverMethod(str, Enum):
    SINGLE_POINT = "single_point"
    TWO_POINT = "two_point"
    UNIFORM = "uniform"
    NONE = "none"


@dataclass
class Population:
    size: int
    organisms: list[str] = field(default_factory=list)
    generation: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Population:
        validate_range(require_field(data, "size", int), "size", min_val=1)
        validate_range(require_field(data, "generation", int), "generation", min_val=0)
        return cls(size=data["size"], organisms=data["organisms"], generation=data["generation"])

    def to_dict(self) -> dict[str, Any]:
        return {"size": self.size, "organisms": self.organisms, "generation": self.generation}


@dataclass
class Selection:
    strategy: SelectionStrategy
    pressure: float
    elitism_rate: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Selection:
        validate_enum_value(require_field(data, "strategy", str), {s.value for s in SelectionStrategy}, "strategy")
        validate_range(require_field(data, "pressure", (int, float)), "pressure", 0.0, 1.0)
        validate_range(require_field(data, "elitism_rate", (int, float)), "elitism_rate", 0.0, 1.0)
        return cls(
            strategy=SelectionStrategy(data["strategy"]),
            pressure=data["pressure"],
            elitism_rate=data["elitism_rate"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "strategy": self.strategy.value,
            "pressure": self.pressure,
            "elitism_rate": self.elitism_rate,
        }


@dataclass
class Crossover:
    method: CrossoverMethod
    rate: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Crossover:
        return cls(method=CrossoverMethod(data["method"]), rate=data["rate"])

    def to_dict(self) -> dict[str, Any]:
        return {"method": self.method.value, "rate": self.rate}


@dataclass
class EngineMutation:
    rate: float
    decay: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> EngineMutation:
        return cls(rate=data["rate"], decay=data["decay"])

    def to_dict(self) -> dict[str, Any]:
        return {"rate": self.rate, "decay": self.decay}


@dataclass
class Termination:
    max_generations: int
    fitness_target: float
    stagnation_limit: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Termination:
        return cls(
            max_generations=data["max_generations"],
            fitness_target=data["fitness_target"],
            stagnation_limit=data["stagnation_limit"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_generations": self.max_generations,
            "fitness_target": self.fitness_target,
            "stagnation_limit": self.stagnation_limit,
        }


@dataclass
class Engine:
    id: str
    name: str
    version: str
    population: Population
    selection: Selection
    crossover: Crossover
    mutation: EngineMutation
    termination: Termination

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Engine:
        validate_uuid(require_field(data, "id", str), "id")
        require_field(data, "name", str)
        validate_semver(require_field(data, "version", str), "version")
        return cls(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            population=Population.from_dict(data["population"]),
            selection=Selection.from_dict(data["selection"]),
            crossover=Crossover.from_dict(data["crossover"]),
            mutation=EngineMutation.from_dict(data["mutation"]),
            termination=Termination.from_dict(data["termination"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "population": self.population.to_dict(),
            "selection": self.selection.to_dict(),
            "crossover": self.crossover.to_dict(),
            "mutation": self.mutation.to_dict(),
            "termination": self.termination.to_dict(),
        }
