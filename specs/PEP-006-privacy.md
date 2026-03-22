# PEP-006: Privacy

| Field   | Value                      |
|---------|----------------------------|
| PEP     | 006                        |
| Title   | Privacy                    |
| Status  | Draft                      |
| Author  | PEP Working Group          |
| Created | 2026-03-22                 |

## Abstract

This specification defines **Privacy Policies** for the PEP ecosystem. A privacy policy declares rules for field-level data protection (redaction, hashing, encryption, omission, generalization), data retention, consent tracking, and audit logging.

## Motivation

Evolutionary data may contain sensitive information — proprietary traits, user-derived features, or confidential fitness scores. Privacy policies provide declarative, enforceable rules that apply consistently across export, logging, and API access paths.

## Specification

### Top-Level Fields

| Field       | Type   | Required | Description                             |
|-------------|--------|----------|-----------------------------------------|
| `id`        | UUID   | Yes      | Unique policy identifier                |
| `version`   | string | Yes      | Semantic version of this policy         |
| `scope`     | enum   | Yes      | What this policy applies to             |
| `rules`     | array  | Yes      | Field-level protection rules            |
| `retention` | object | Yes      | Data lifecycle configuration            |
| `consent`   | object | Yes      | Consent tracking                        |
| `audit`     | object | Yes      | Audit logging configuration             |

### `scope` Enum

`"organism"` | `"judge"` | `"engine"` | `"event"` | `"global"`

### `rules` Array Items (Rule)

| Field       | Type   | Required | Description                                      |
|-------------|--------|----------|--------------------------------------------------|
| `field`     | string | Yes      | Dot-path to the target field (e.g. `genome.traits`) |
| `action`    | enum   | Yes      | `"redact"` \| `"hash"` \| `"encrypt"` \| `"omit"` \| `"generalize"` |
| `condition` | object | No       | When to apply the rule                           |

**Condition**: `{ context: "export" | "log" | "api" | "always" }`

### `retention` Object

| Field               | Type    | Required | Constraints | Description                    |
|---------------------|---------|----------|-------------|--------------------------------|
| `max_age_days`      | integer | Yes      | > 0         | Maximum data age               |
| `auto_purge`        | boolean | Yes      | —           | Automatically delete expired   |
| `archive_after_days`| integer | No       | > 0         | Move to cold storage after N days |

### `consent` Object

| Field        | Type     | Required | Description                        |
|--------------|----------|----------|------------------------------------|
| `required`   | boolean  | Yes      | Whether consent is required        |
| `granted_by` | UUID     | No       | Who granted consent                |
| `granted_at` | ISO 8601 | No       | When consent was granted           |

### `audit` Object

| Field                 | Type    | Description                              |
|-----------------------|---------|------------------------------------------|
| `log_access`          | boolean | Log every read access                    |
| `log_mutations`       | boolean | Log every data modification              |
| `require_justification`| boolean | Require a reason for access             |

## Example

```json
{
  "id": "deadbeef-cafe-babe-dead-beefcafebabe",
  "version": "1.0.0",
  "scope": "organism",
  "rules": [
    { "field": "genome.traits", "action": "redact", "condition": { "context": "export" } },
    { "field": "metadata.tags", "action": "omit" }
  ],
  "retention": { "max_age_days": 365, "auto_purge": true, "archive_after_days": 90 },
  "consent": { "required": true, "granted_by": "a1b2c3d4-e5f6-7890-abcd-ef1234567890", "granted_at": "2026-01-01T00:00:00Z" },
  "audit": { "log_access": true, "log_mutations": true, "require_justification": false }
}
```

## Conformance Requirements

1. `scope` MUST be one of the five defined values.
2. `rules[].action` MUST be one of the five defined values.
3. `rules[].condition.context`, when present, MUST be one of the four defined values.
4. `retention.max_age_days` MUST be > 0.
5. Implementations MUST apply rules in array order (first match wins).
6. When `consent.required` is true, operations SHOULD verify `granted_by` and `granted_at` are present.

## References

- [PEP-004 Event Log](./PEP-004-event-log.md)
- [PEP-005 Sharing](./PEP-005-sharing.md)
- [GDPR Article 17 — Right to Erasure](https://gdpr-info.eu/art-17-gdpr/)
