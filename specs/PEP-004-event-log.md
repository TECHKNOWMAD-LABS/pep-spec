# PEP-004: Event Log

| Field   | Value                      |
|---------|----------------------------|
| PEP     | 004                        |
| Title   | Event Log                  |
| Status  | Draft                      |
| Author  | PEP Working Group          |
| Created | 2026-03-22                 |

## Abstract

This specification defines the **Event Log**, an immutable, append-only record of all significant actions in the PEP ecosystem. Events enable auditing, replay, debugging, and cross-component correlation.

## Motivation

Evolutionary processes are inherently complex and non-deterministic. A structured event log provides observability into every mutation, evaluation, generation transition, and agent action. The checksum field ensures tamper-evidence.

## Specification

### Top-Level Fields

| Field            | Type    | Required | Description                                    |
|------------------|---------|----------|------------------------------------------------|
| `id`             | UUID    | Yes      | Unique event identifier                        |
| `timestamp`      | ISO 8601| Yes      | When the event occurred                        |
| `type`           | enum    | Yes      | Event type (see table below)                   |
| `source`         | object  | Yes      | Component that emitted the event               |
| `payload`        | object  | Yes      | Event-specific data                            |
| `sequence`       | integer | Yes      | Monotonically increasing counter (>= 0)        |
| `correlation_id` | UUID    | No       | Groups related events                          |
| `checksum`       | string  | Yes      | SHA-256 hex digest of the payload              |

### `type` Enum

| Value                    | Emitted By |
|--------------------------|------------|
| `organism.created`       | engine     |
| `organism.mutated`       | engine     |
| `organism.evaluated`     | judge      |
| `organism.died`          | engine     |
| `generation.started`     | engine     |
| `generation.completed`   | engine     |
| `engine.started`         | engine     |
| `engine.stopped`         | engine     |
| `judge.verdict`          | judge      |
| `sharing.exported`       | sharing    |
| `sharing.imported`       | sharing    |
| `privacy.redacted`       | privacy    |
| `agent.action`           | agent      |

### `source` Object

| Field       | Type | Description                                             |
|-------------|------|---------------------------------------------------------|
| `component` | enum | `"organism"` \| `"judge"` \| `"engine"` \| `"sharing"` \| `"privacy"` \| `"agent"` |
| `id`        | UUID | ID of the emitting component instance                   |

### `checksum`

The checksum MUST be a 64-character lowercase hexadecimal string representing the SHA-256 digest of the canonical JSON serialization of the `payload` field.

## Example

```json
{
  "id": "11111111-2222-3333-4444-555555555555",
  "timestamp": "2026-03-22T14:30:00Z",
  "type": "organism.mutated",
  "source": { "component": "engine", "id": "d4e5f6a7-b8c9-0123-def0-456789abcdef" },
  "payload": { "organism_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "gene": "speed", "operation": "modify" },
  "sequence": 42,
  "correlation_id": "99999999-8888-7777-6666-555544443333",
  "checksum": "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
}
```

## Conformance Requirements

1. Events MUST be append-only; implementations MUST NOT allow deletion or modification.
2. `sequence` MUST be monotonically increasing within a single source.
3. `checksum` MUST be a valid 64-character hex SHA-256 digest.
4. `correlation_id`, when present, MUST be a valid UUID.
5. `type` and `source.component` MUST be one of the defined enum values.

## References

- [PEP-001 Organism](./PEP-001-organism.md)
- [PEP-002 Judge](./PEP-002-judge.md)
- [PEP-003 Engine](./PEP-003-engine.md)
- [RFC 6234 — SHA-256](https://www.rfc-editor.org/rfc/rfc6234)
