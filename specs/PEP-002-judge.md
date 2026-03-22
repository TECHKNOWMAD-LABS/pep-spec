# PEP-002: Judge

| Field   | Value                      |
|---------|----------------------------|
| PEP     | 002                        |
| Title   | Judge                      |
| Status  | Draft                      |
| Author  | PEP Working Group          |
| Created | 2026-03-22                 |

## Abstract

This specification defines the **Judge**, an evaluator that assesses organisms against weighted criteria and produces verdicts. Judges are the fitness function abstraction in the PEP ecosystem.

## Motivation

Evolutionary systems require fitness evaluation. By formalizing the judge as a first-class entity with versioned criteria, configurable execution parameters, and structured verdicts, PEP enables reproducible evaluation pipelines and composable fitness landscapes.

## Specification

### Top-Level Fields

| Field      | Type     | Required | Description                               |
|------------|----------|----------|-------------------------------------------|
| `id`       | UUID     | Yes      | Unique identifier                         |
| `name`     | string   | Yes      | Human-readable name (1-128 chars)         |
| `version`  | string   | Yes      | Semantic version                          |
| `criteria` | array    | Yes      | Evaluation criteria (min 1 item)          |
| `verdict`  | object   | Yes      | Evaluation result                         |
| `config`   | object   | Yes      | Execution configuration                   |

### `criteria` Array Items (Criterion)

| Field       | Type   | Description                                         |
|-------------|--------|-----------------------------------------------------|
| `name`      | string | Criterion name                                      |
| `weight`    | float  | Importance weight [0, 1]                             |
| `threshold` | float  | Minimum passing score [0, 1]                         |
| `metric`    | enum   | `"accuracy"` \| `"latency"` \| `"cost"` \| `"safety"` \| `"creativity"` |

### `verdict` Object

| Field         | Type            | Description                              |
|---------------|-----------------|------------------------------------------|
| `organism_id` | UUID            | The organism being evaluated             |
| `score`       | float [0, 1]   | Aggregate fitness score                  |
| `passed`      | boolean         | Whether the organism passed evaluation   |
| `details`     | array[Detail]   | Per-criterion breakdown                  |

**Detail**: `{ criterion: string, score: float, passed: boolean }`

### `config` Object

| Field         | Type    | Constraints    | Description                     |
|---------------|---------|----------------|---------------------------------|
| `max_retries` | integer | >= 0           | Retry count on evaluation failure |
| `timeout_ms`  | integer | > 0            | Maximum evaluation time in ms    |
| `parallel`    | boolean | —              | Whether criteria run in parallel |

## Example

```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "name": "safety-judge",
  "version": "2.0.0",
  "criteria": [
    { "name": "safety-score", "weight": 0.8, "threshold": 0.95, "metric": "safety" },
    { "name": "response-time", "weight": 0.2, "threshold": 0.5, "metric": "latency" }
  ],
  "verdict": {
    "organism_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "score": 0.91,
    "passed": true,
    "details": [
      { "criterion": "safety-score", "score": 0.97, "passed": true },
      { "criterion": "response-time", "score": 0.68, "passed": true }
    ]
  },
  "config": { "max_retries": 2, "timeout_ms": 10000, "parallel": true }
}
```

## Conformance Requirements

1. The `criteria` array MUST contain at least one item.
2. `weight` and `threshold` MUST be in [0, 1].
3. `metric` MUST be one of the five defined values.
4. `verdict.organism_id` MUST be a valid UUID.
5. `verdict.score` MUST be in [0, 1].
6. `config.max_retries` MUST be >= 0; `config.timeout_ms` MUST be > 0.

## References

- [PEP-001 Organism](./PEP-001-organism.md)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core)
