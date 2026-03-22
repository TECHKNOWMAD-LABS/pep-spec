# PEP-005: Sharing

| Field   | Value                      |
|---------|----------------------------|
| PEP     | 005                        |
| Title   | Sharing                    |
| Status  | Draft                      |
| Author  | PEP Working Group          |
| Created | 2026-03-22                 |

## Abstract

This specification defines the **Sharing** protocol for importing and exporting organisms, genomes, and evolutionary artifacts between PEP-compliant systems. It covers format negotiation, transport, integrity verification, and access control.

## Motivation

Evolutionary programs become more powerful when organisms can migrate between populations, engines, and organizations. The sharing protocol ensures that exported artifacts are self-describing, integrity-verified, and permission-controlled.

## Specification

### Top-Level Fields

| Field         | Type   | Required | Description                            |
|---------------|--------|----------|----------------------------------------|
| `id`          | UUID   | Yes      | Unique sharing manifest ID             |
| `format`      | enum   | Yes      | Serialization format                   |
| `source`      | object | Yes      | Where the artifact came from           |
| `target`      | object | Yes      | Where the artifact is going            |
| `content`     | object | Yes      | What is included                       |
| `integrity`   | object | Yes      | Hash and optional signature            |
| `permissions` | object | Yes      | Access control                         |

### `format` Enum

`"pep-native"` | `"onnx"` | `"safetensors"` | `"json"` | `"custom"`

### `source` Object

| Field         | Type    | Description                     |
|---------------|---------|---------------------------------|
| `organism_id` | UUID    | Source organism                  |
| `engine_id`   | UUID    | Engine that produced it          |
| `generation`  | integer | Generation number (>= 0)        |

### `target` Object

| Field      | Type   | Description                                        |
|------------|--------|----------------------------------------------------|
| `uri`      | string | Destination URI                                    |
| `protocol` | enum   | `"https"` \| `"ipfs"` \| `"s3"` \| `"local"`      |

### `content` Object

| Field        | Type    | Description                        |
|--------------|---------|------------------------------------|
| `genome`     | boolean | Include genome data                |
| `phenotype`  | boolean | Include phenotype data             |
| `history`    | boolean | Include evolutionary history       |
| `size_bytes` | integer | Total size in bytes (>= 0)         |

### `integrity` Object

| Field       | Type   | Required | Description                              |
|-------------|--------|----------|------------------------------------------|
| `algorithm` | enum   | Yes      | `"sha256"` \| `"sha512"` \| `"blake3"`   |
| `hash`      | string | Yes      | Hex digest (min 1 char)                  |
| `signature` | string | No       | Optional cryptographic signature         |

### `permissions` Object

| Field               | Type         | Required | Description                        |
|---------------------|--------------|----------|------------------------------------|
| `public`            | boolean      | Yes      | Publicly accessible                |
| `allowed_consumers` | array[UUID]  | Yes      | Authorized consumer IDs            |
| `expires_at`        | ISO 8601     | No       | Permission expiration              |

## Example

```json
{
  "id": "aaaabbbb-cccc-dddd-eeee-ffffffffffff",
  "format": "pep-native",
  "source": {
    "organism_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "engine_id": "d4e5f6a7-b8c9-0123-def0-456789abcdef",
    "generation": 42
  },
  "target": { "uri": "https://registry.pep-spec.dev/artifacts/42", "protocol": "https" },
  "content": { "genome": true, "phenotype": true, "history": false, "size_bytes": 204800 },
  "integrity": { "algorithm": "sha256", "hash": "e3b0c44298fc1c149afbf4c8996fb924..." },
  "permissions": { "public": false, "allowed_consumers": ["11111111-2222-3333-4444-555555555555"] }
}
```

## Conformance Requirements

1. `format` MUST be one of the defined values.
2. `integrity.hash` MUST NOT be empty.
3. `content.size_bytes` MUST be >= 0.
4. All UUID fields MUST be valid UUID format.
5. `target.uri` MUST be a valid URI.

## References

- [PEP-001 Organism](./PEP-001-organism.md)
- [PEP-003 Engine](./PEP-003-engine.md)
- [PEP-006 Privacy](./PEP-006-privacy.md)
