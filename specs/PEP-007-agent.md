# PEP-007: Agent

| Field   | Value                      |
|---------|----------------------------|
| PEP     | 007                        |
| Title   | Agent                      |
| Status  | Draft                      |
| Author  | PEP Working Group          |
| Created | 2026-03-22                 |

## Abstract

This specification defines the **Agent**, an autonomous actor that operates within the PEP ecosystem. Agents have defined roles, capabilities, bindings to other components, rate-limited policies, and observable state.

## Motivation

Complex evolutionary systems benefit from autonomous agents that can evolve organisms, guard population health, explore parameter spaces, harvest results, or orchestrate multi-engine pipelines. The agent spec provides a uniform way to declare, constrain, and monitor these actors.

## Specification

### Top-Level Fields

| Field          | Type   | Required | Description                           |
|----------------|--------|----------|---------------------------------------|
| `id`           | UUID   | Yes      | Unique agent identifier               |
| `name`         | string | Yes      | Human-readable name (1-128 chars)     |
| `version`      | string | Yes      | Semantic version                      |
| `role`         | enum   | Yes      | Agent's primary role                  |
| `capabilities` | array  | Yes      | List of capability strings            |
| `bindings`     | object | Yes      | References to bound components        |
| `policy`       | object | Yes      | Behavioral constraints                |
| `state`        | object | Yes      | Current runtime state                 |

### `role` Enum

| Value          | Description                                    |
|----------------|------------------------------------------------|
| `evolver`      | Performs mutations and crossover                |
| `guardian`     | Monitors population health and enforces rules  |
| `explorer`     | Searches parameter spaces                      |
| `harvester`    | Collects and exports results                   |
| `orchestrator` | Coordinates multiple engines or agents         |

### `bindings` Object

| Field          | Type        | Required | Description                     |
|----------------|-------------|----------|---------------------------------|
| `engine_id`    | UUID        | No       | Bound engine                    |
| `organism_ids` | array[UUID] | Yes      | Bound organisms                 |
| `judge_ids`    | array[UUID] | Yes      | Bound judges                    |

### `policy` Object

| Field                    | Type          | Constraints | Description                    |
|--------------------------|---------------|-------------|--------------------------------|
| `max_actions_per_minute` | integer       | > 0         | Rate limit                     |
| `require_approval`       | boolean       | —           | Human-in-the-loop gate         |
| `allowed_actions`        | array[string] | —           | Whitelist of permitted actions |
| `denied_actions`         | array[string] | —           | Blacklist of forbidden actions |

### `state` Object

| Field            | Type     | Required | Description                       |
|------------------|----------|----------|-----------------------------------|
| `status`         | enum     | Yes      | `"idle"` \| `"active"` \| `"suspended"` \| `"terminated"` |
| `current_task`   | string   | No       | Description of current work       |
| `last_action_at` | ISO 8601 | No       | Timestamp of last action          |
| `error_count`    | integer  | Yes      | Cumulative error count (>= 0)    |

## Example

```json
{
  "id": "abcdef01-2345-6789-abcd-ef0123456789",
  "name": "genome-explorer",
  "version": "1.0.0",
  "role": "explorer",
  "capabilities": ["mutate", "analyze", "report"],
  "bindings": {
    "engine_id": "d4e5f6a7-b8c9-0123-def0-456789abcdef",
    "organism_ids": ["a1b2c3d4-e5f6-7890-abcd-ef1234567890"],
    "judge_ids": []
  },
  "policy": {
    "max_actions_per_minute": 120,
    "require_approval": false,
    "allowed_actions": ["mutate", "analyze"],
    "denied_actions": ["delete", "terminate"]
  },
  "state": {
    "status": "active",
    "current_task": "exploring mutation space for gen-42",
    "last_action_at": "2026-03-22T14:30:00Z",
    "error_count": 0
  }
}
```

## Conformance Requirements

1. `role` MUST be one of the five defined values.
2. `state.status` MUST be one of the four defined values.
3. `policy.max_actions_per_minute` MUST be > 0.
4. `state.error_count` MUST be >= 0.
5. All UUID fields MUST be valid UUID format.
6. If `denied_actions` contains an action, it MUST take precedence over `allowed_actions`.

## References

- [PEP-001 Organism](./PEP-001-organism.md)
- [PEP-002 Judge](./PEP-002-judge.md)
- [PEP-003 Engine](./PEP-003-engine.md)
- [PEP-004 Event Log](./PEP-004-event-log.md)
