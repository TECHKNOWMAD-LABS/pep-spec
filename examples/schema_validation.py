#!/usr/bin/env python3
"""Example: Validate data against PEP JSON Schemas.

Demonstrates:
- Loading JSON Schema files
- Validating valid and invalid payloads
- Getting detailed validation error messages
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import jsonschema


SCHEMAS_DIR = PROJECT_ROOT / "schemas"


def load_schema(name: str) -> dict:
    """Load a JSON Schema by component name."""
    path = SCHEMAS_DIR / f"{name}.schema.json"
    with open(path) as f:
        return json.load(f)


def validate_and_report(name: str, data: dict, schema: dict) -> bool:
    """Validate data against schema and print result."""
    try:
        jsonschema.validate(data, schema)
        print(f"  [PASS] {name}")
        return True
    except jsonschema.ValidationError as e:
        print(f"  [FAIL] {name}: {e.message}")
        return False


def main() -> None:
    # ── Valid organism ────────────────────────────────────────────────
    print("=== Organism Schema Validation ===")
    organism_schema = load_schema("organism")

    valid_organism = {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "name": "test-organism",
        "version": "1.0.0",
        "genome": {
            "traits": [{"name": "speed", "value": 42, "weight": 0.8}],
            "mutations": [],
        },
        "phenotype": {"capabilities": ["run"], "constraints": []},
        "metadata": {
            "created_at": "2026-01-15T10:30:00Z",
            "updated_at": "2026-01-15T10:30:00Z",
            "tags": [],
            "lineage": [],
        },
        "status": "alive",
    }
    validate_and_report("valid organism", valid_organism, organism_schema)

    # ── Invalid: missing required field ───────────────────────────────
    invalid_no_id = {k: v for k, v in valid_organism.items() if k != "id"}
    validate_and_report("missing 'id'", invalid_no_id, organism_schema)

    # ── Invalid: bad status enum ──────────────────────────────────────
    invalid_status = {**valid_organism, "status": "flying"}
    validate_and_report("invalid status", invalid_status, organism_schema)

    # ── Invalid: trait weight out of range ────────────────────────────
    invalid_weight = {
        **valid_organism,
        "genome": {
            "traits": [{"name": "speed", "value": 42, "weight": 1.5}],
            "mutations": [],
        },
    }
    validate_and_report("weight > 1.0", invalid_weight, organism_schema)

    # ── Judge schema ──────────────────────────────────────────────────
    print("\n=== Judge Schema Validation ===")
    judge_schema = load_schema("judge")

    valid_judge = {
        "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        "name": "test-judge",
        "version": "1.0.0",
        "criteria": [
            {"name": "accuracy", "weight": 0.7, "threshold": 0.9, "metric": "accuracy"},
        ],
        "verdict": {
            "organism_id": "b2c3d4e5-f6a7-8901-bcde-f12345678901",
            "score": 0.85,
            "passed": True,
            "details": [],
        },
        "config": {"max_retries": 3, "timeout_ms": 5000, "parallel": True},
    }
    validate_and_report("valid judge", valid_judge, judge_schema)

    # ── Invalid: empty criteria ───────────────────────────────────────
    invalid_judge = {**valid_judge, "criteria": []}
    validate_and_report("empty criteria", invalid_judge, judge_schema)

    print("\n=== All validations complete ===")


if __name__ == "__main__":
    main()
