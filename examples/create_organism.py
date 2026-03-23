#!/usr/bin/env python3
"""Example: Create and validate a PEP organism.

Demonstrates:
- Building an Organism from scratch using dataclasses
- Serializing to dict (JSON-compatible)
- Validating against the JSON Schema
- Round-trip deserialization
"""

import json
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import jsonschema

from stubs.organism import (
    Constraint,
    Genome,
    Mutation,
    Organism,
    OrganismMetadata,
    OrganismStatus,
    Phenotype,
    Trait,
)


def main() -> None:
    # 1. Build an organism
    organism = Organism(
        id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        name="speed-runner-v1",
        version="1.0.0",
        genome=Genome(
            traits=[
                Trait(name="speed", value=42.0, weight=0.8),
                Trait(name="endurance", value=85.0, weight=0.6),
            ],
            mutations=[
                Mutation(gene="speed", operation="modify", payload={"delta": 5}),
            ],
        ),
        phenotype=Phenotype(
            capabilities=["run", "jump", "climb"],
            constraints=[
                Constraint(resource="memory", limit=1024.0),
                Constraint(resource="cpu_cores", limit=4.0),
            ],
        ),
        metadata=OrganismMetadata(
            created_at="2026-01-15T10:30:00Z",
            updated_at="2026-01-15T10:30:00Z",
            tags=["fast", "generation-42"],
            lineage=[],
        ),
        status=OrganismStatus.ALIVE,
    )

    # 2. Serialize to dict
    data = organism.to_dict()
    print("=== Organism (dict) ===")
    print(json.dumps(data, indent=2))

    # 3. Validate against JSON Schema
    schema_path = PROJECT_ROOT / "schemas" / "organism.schema.json"
    with open(schema_path) as f:
        schema = json.load(f)
    jsonschema.validate(data, schema)
    print("\n[OK] Schema validation passed")

    # 4. Round-trip: deserialize back
    restored = Organism.from_dict(data)
    assert restored.to_dict() == data
    print("[OK] Round-trip serialization verified")
    print(f"\nOrganism '{restored.name}' has {len(restored.genome.traits)} traits")


if __name__ == "__main__":
    main()
