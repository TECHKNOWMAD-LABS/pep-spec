# PEP-001: Organism

| Field   | Value                      |
|---------|----------------------------|
| PEP     | 001                        |
| Title   | Organism                   |
| Status  | Draft                      |
| Author  | PEP Working Group          |
| Created | 2026-03-22                 |

## Abstract

This specification defines the **Organism**, the fundamental evolvable unit in the PEP ecosystem. An organism encapsulates a genome (traits and mutations), a phenotype (capabilities and constraints), lifecycle metadata, and a status field governing its participation in evolutionary processes.

## Motivation

Every evolutionary system requires a well-defined individual. The Organism spec provides a portable, self-describing representation that engines, judges, sharing protocols, and agents can operate on without ambiguity. By standardizing the organism structure, we enable interoperability across heterogeneous evolutionary platforms.

## Specification

### Top-Level Fields

| Field       | Type     | Required | Description                                     |
|-------------|----------|----------|-------------------------------------------------|
| `id`        | UUID     | Yes      | Unique identifier (UUID v4, lowercase hex)      |
| `name`      | string   | Yes      | Human-readable name (1-128 characters)           |
| `version`   | string   | Yes      | Semantic version (e.g. `1.0.0`)                  |
| `genome`    | object   | Yes      | Genetic material — traits and mutations          |
| `phenotype` | object   | Yes      | Observable characteristics and resource limits   |
| `metadata`  | object   | Yes      | Timestamps, tags, and lineage                    |
| `status`    | enum     | Yes      | Lifecycle state                                  |

### `genome` Object

| Field       | Type           | Description                                    |
|-------------|----------------|------------------------------------------------|
| `traits`    | array[Trait]   | List of named traits with values and weights   |
| `mutations` | array[Mutation]| List of pending or applied mutations           |

**Trait**: `{ name: string, value: any, weight: float [0,1] }`

**Mutation**: `{ gene: string, operation: "add"|"remove"|"modify", payload: any }`

### `phenotype` Object

| Field          | Type              | Description                          |
|----------------|-------------------|--------------------------------------|
| `capabilities` | array[string]     | What the organism can do             |
| `constraints`  | array[Constraint] | Resource limits                      |

**Constraint**: `{ resource: string, limit: number }`

### `metadata` Object

| Field        | Type           | Description                              |
|--------------|----------------|------------------------------------------|
| `created_at` | ISO 8601       | When the organism was created            |
| `updated_at` | ISO 8601       | When the organism was last modified      |
| `tags`       | array[string]  | Free-form labels                         |
| `lineage`    | array[UUID]    | Ancestor organism IDs (oldest first)     |

### `status` Enum

| Value     | Meaning                                      |
|-----------|----------------------------------------------|
| `embryo`  | Created but not yet participating             |
| `alive`   | Active participant in the population          |
| `dormant` | Temporarily suspended                        |
| `dead`    | Permanently removed from the population      |

## Example

```json
{
  "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "name": "alpha-predator",
  "version": "1.2.0",
  "genome": {
    "traits": [
      { "name": "speed", "value": 88, "weight": 0.7 },
      { "name": "stealth", "value": true, "weight": 0.3 }
    ],
    "mutations": [
      { "gene": "speed", "operation": "modify", "payload": { "delta": 5 } }
    ]
  },
  "phenotype": {
    "capabilities": ["hunt", "evade"],
    "constraints": [
      { "resource": "memory_mb", "limit": 512 }
    ]
  },
  "metadata": {
    "created_at": "2026-01-01T00:00:00Z",
    "updated_at": "2026-03-15T12:00:00Z",
    "tags": ["predator", "gen-42"],
    "lineage": ["00000000-0000-0000-0000-000000000001"]
  },
  "status": "alive"
}
```

## Conformance Requirements

1. Implementations MUST validate the `id` field as a lowercase UUID v4 string.
2. The `name` field MUST be between 1 and 128 characters.
3. The `version` field MUST conform to Semantic Versioning 2.0.0.
4. Trait `weight` values MUST be in the range [0, 1].
5. Mutation `operation` MUST be one of `add`, `remove`, `modify`.
6. `status` MUST be one of the four defined enum values.
7. No additional properties are allowed at any nesting level.

## References

- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core)
- [Semantic Versioning 2.0.0](https://semver.org/)
- [RFC 4122 — UUID](https://www.rfc-editor.org/rfc/rfc4122)
