# PEP-003: Engine

| Field   | Value                      |
|---------|----------------------------|
| PEP     | 003                        |
| Title   | Engine                     |
| Status  | Draft                      |
| Author  | PEP Working Group          |
| Created | 2026-03-22                 |

## Abstract

This specification defines the **Engine**, the orchestrator of the evolutionary process. An engine manages a population of organisms through generations using configurable selection, crossover, mutation, and termination strategies.

## Motivation

The engine is the control plane of evolution. Standardizing its configuration enables reproducible experiments, composable pipelines, and interoperable tooling. Different selection pressures, crossover methods, and termination conditions can be swapped declaratively.

## Specification

### Top-Level Fields

| Field         | Type   | Required | Description                           |
|---------------|--------|----------|---------------------------------------|
| `id`          | UUID   | Yes      | Unique identifier                     |
| `name`        | string | Yes      | Engine name (1-128 chars)             |
| `version`     | string | Yes      | Semantic version                      |
| `population`  | object | Yes      | Current population state              |
| `selection`   | object | Yes      | Selection strategy configuration      |
| `crossover`   | object | Yes      | Crossover configuration               |
| `mutation`    | object | Yes      | Mutation configuration                |
| `termination` | object | Yes      | Stopping conditions                   |

### `population` Object

| Field        | Type         | Constraints | Description                     |
|--------------|--------------|-------------|---------------------------------|
| `size`       | integer      | > 0         | Target population size          |
| `organisms`  | array[UUID]  | —           | Current organism IDs            |
| `generation` | integer      | >= 0        | Current generation number       |

### `selection` Object

| Field          | Type   | Constraints | Description                      |
|----------------|--------|-------------|----------------------------------|
| `strategy`     | enum   | —           | `"tournament"` \| `"roulette"` \| `"rank"` \| `"elite"` |
| `pressure`     | float  | [0, 1]      | Selection pressure               |
| `elitism_rate` | float  | [0, 1]      | Fraction preserved unchanged     |

### `crossover` Object

| Field    | Type  | Constraints | Description                                  |
|----------|-------|-------------|----------------------------------------------|
| `method` | enum  | —           | `"single_point"` \| `"two_point"` \| `"uniform"` \| `"none"` |
| `rate`   | float | [0, 1]      | Probability of crossover per pair            |

### `mutation` Object

| Field   | Type  | Constraints | Description                          |
|---------|-------|-------------|--------------------------------------|
| `rate`  | float | [0, 1]      | Probability of mutation per gene     |
| `decay` | float | [0, 1]      | Rate at which mutation rate decreases |

### `termination` Object

| Field              | Type    | Constraints | Description                           |
|--------------------|---------|-------------|---------------------------------------|
| `max_generations`  | integer | > 0         | Hard limit on generations             |
| `fitness_target`   | float   | [0, 1]      | Stop when best fitness reaches this   |
| `stagnation_limit` | integer | > 0         | Stop after N generations without gain |

## Example

```json
{
  "id": "d4e5f6a7-b8c9-0123-def0-456789abcdef",
  "name": "main-evolver",
  "version": "3.0.0",
  "population": {
    "size": 200,
    "organisms": [],
    "generation": 0
  },
  "selection": { "strategy": "tournament", "pressure": 0.75, "elitism_rate": 0.05 },
  "crossover": { "method": "two_point", "rate": 0.85 },
  "mutation": { "rate": 0.02, "decay": 0.005 },
  "termination": { "max_generations": 1000, "fitness_target": 0.99, "stagnation_limit": 100 }
}
```

## Conformance Requirements

1. `population.size` MUST be > 0.
2. All organism IDs in `population.organisms` MUST be valid UUIDs.
3. All float fields with range [0, 1] MUST be enforced.
4. `termination.max_generations` and `termination.stagnation_limit` MUST be > 0.
5. Enum values MUST match exactly (case-sensitive).

## References

- [PEP-001 Organism](./PEP-001-organism.md)
- [PEP-002 Judge](./PEP-002-judge.md)
