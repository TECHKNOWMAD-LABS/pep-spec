"""PEP-001 Organism — the fundamental evolvable unit."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from stubs.validation import (
    ValidationError, require_field, validate_uuid, validate_semver,
    validate_range, validate_enum_value, validate_string_not_empty,
)


class OrganismStatus(str, Enum):
    EMBRYO = "embryo"
    ALIVE = "alive"
    DORMANT = "dormant"
    DEAD = "dead"


@dataclass
class Trait:
    name: str
    value: Any
    weight: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Trait:
        require_field(data, "name", str)
        require_field(data, "weight", (int, float))
        validate_range(data["weight"], "weight", min_val=0.0, max_val=1.0)
        return cls(name=data["name"], value=data["value"], weight=data["weight"])

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "value": self.value, "weight": self.weight}


@dataclass
class Mutation:
    gene: str
    operation: str  # "add" | "remove" | "modify"
    payload: Any

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Mutation:
        require_field(data, "gene", str)
        validate_enum_value(
            require_field(data, "operation", str),
            {"add", "remove", "modify"}, "operation",
        )
        return cls(gene=data["gene"], operation=data["operation"], payload=data["payload"])

    def to_dict(self) -> dict[str, Any]:
        return {"gene": self.gene, "operation": self.operation, "payload": self.payload}


@dataclass
class Genome:
    traits: list[Trait] = field(default_factory=list)
    mutations: list[Mutation] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Genome:
        return cls(
            traits=[Trait.from_dict(t) for t in data["traits"]],
            mutations=[Mutation.from_dict(m) for m in data["mutations"]],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "traits": [t.to_dict() for t in self.traits],
            "mutations": [m.to_dict() for m in self.mutations],
        }


@dataclass
class Constraint:
    resource: str
    limit: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Constraint:
        return cls(resource=data["resource"], limit=data["limit"])

    def to_dict(self) -> dict[str, Any]:
        return {"resource": self.resource, "limit": self.limit}


@dataclass
class Phenotype:
    capabilities: list[str] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Phenotype:
        return cls(
            capabilities=data["capabilities"],
            constraints=[Constraint.from_dict(c) for c in data["constraints"]],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "capabilities": self.capabilities,
            "constraints": [c.to_dict() for c in self.constraints],
        }


@dataclass
class OrganismMetadata:
    created_at: str
    updated_at: str
    tags: list[str] = field(default_factory=list)
    lineage: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OrganismMetadata:
        return cls(
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            tags=data["tags"],
            lineage=data["lineage"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "tags": self.tags,
            "lineage": self.lineage,
        }


@dataclass
class Organism:
    id: str
    name: str
    version: str
    genome: Genome
    phenotype: Phenotype
    metadata: OrganismMetadata
    status: OrganismStatus

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Organism:
        validate_uuid(require_field(data, "id", str), "id")
        validate_string_not_empty(require_field(data, "name", str), "name", max_length=128)
        validate_semver(require_field(data, "version", str), "version")
        require_field(data, "genome", dict)
        require_field(data, "phenotype", dict)
        require_field(data, "metadata", dict)
        validate_enum_value(
            require_field(data, "status", str),
            {s.value for s in OrganismStatus}, "status",
        )
        return cls(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            genome=Genome.from_dict(data["genome"]),
            phenotype=Phenotype.from_dict(data["phenotype"]),
            metadata=OrganismMetadata.from_dict(data["metadata"]),
            status=OrganismStatus(data["status"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "genome": self.genome.to_dict(),
            "phenotype": self.phenotype.to_dict(),
            "metadata": self.metadata.to_dict(),
            "status": self.status.value,
        }
