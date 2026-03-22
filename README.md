# PEP — Protocol for Evolutionary Programs

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12](https://img.shields.io/badge/Python-3.12-3776ab.svg)](https://www.python.org/downloads/release/python-3120/)
[![Tests](https://img.shields.io/badge/Tests-125%20passing-brightgreen.svg)](conformance/)

A formal specification for AI agent ecosystems built around evolutionary computation. PEP defines seven interoperating components that together enable reproducible, observable, and privacy-aware evolutionary processes.

## Features

- **Formal JSON Schema (draft 2020-12)** for all seven components — validate any conforming implementation
- **Python 3.12 dataclass stubs** with `from_dict` / `to_dict` and full type annotations
- **TypeScript type definitions** for browser and Node.js consumers
- **125 conformance tests** covering schema validation, round-trip serialization, edge cases, and cross-spec references
- **Immutable event log** (PEP-004) providing a tamper-evident audit trail for every ecosystem action
- **Field-level privacy controls** (PEP-006) with retention policy, consent tracking, and access-control rules

## Specifications

| PEP | Name | Description |
|-----|------|-------------|
| [001](specs/PEP-001-organism.md) | Organism | The fundamental evolvable unit with genome, phenotype, and lifecycle |
| [002](specs/PEP-002-judge.md) | Judge | Evaluates organisms against weighted criteria and produces verdicts |
| [003](specs/PEP-003-engine.md) | Engine | Orchestrates evolution with selection, crossover, mutation, and termination |
| [004](specs/PEP-004-event-log.md) | Event Log | Immutable, append-only audit trail for all ecosystem actions |
| [005](specs/PEP-005-sharing.md) | Sharing | Import/export protocol with integrity verification and access control |
| [006](specs/PEP-006-privacy.md) | Privacy | Field-level data protection, retention, consent, and audit rules |
| [007](specs/PEP-007-agent.md) | Agent | Autonomous actors with roles, capabilities, policies, and observable state |

## Quick Start

**Install:**

```bash
pip install jsonschema
pip install pytest pytest-cov  # for running tests
```

**Run the conformance suite:**

```bash
pytest conformance/ -v
# 125 passed in <1s
```

**Instantiate and round-trip an Organism:**

```python
import sys
sys.path.insert(0, ".")

from stubs.organism import Organism

data = {
    "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "name": "my-organism",
    "version": "1.0.0",
    "genome": {"traits": [], "mutations": []},
    "phenotype": {"capabilities": [], "constraints": []},
    "metadata": {
        "created_at": "2026-01-01T00:00:00Z",
        "updated_at": "2026-01-01T00:00:00Z",
        "tags": [],
        "lineage": []
    },
    "status": "embryo"
}

org = Organism.from_dict(data)
assert org.to_dict() == data   # round-trip verified
```

**Validate against the JSON Schema:**

```python
import json, jsonschema

with open("schemas/organism.schema.json") as f:
    schema = json.load(f)

jsonschema.validate(data, schema)  # raises jsonschema.ValidationError on invalid input
```

## Architecture

```
pep-spec/
  specs/           # Authoritative Markdown specifications (PEP-001 — PEP-007)
  schemas/         # JSON Schema (draft 2020-12) — one file per spec
  types/           # TypeScript type definitions (index.d.ts)
  stubs/           # Python 3.12 dataclass stubs with from_dict / to_dict
  conformance/     # 125 pytest conformance tests (schema, serialization, cross-spec)
  pyproject.toml   # Build config, dependencies, pytest + mypy settings
  LICENSE          # MIT
```

The specs are the single source of truth. Schemas, stubs, and TypeScript types are generated artifacts that must conform to the spec. The conformance suite enforces this mechanically on every commit.

**Component interaction:**

```
Agent (PEP-007)
  └─ drives ──► Engine (PEP-003)
                  ├─ selects / mutates ──► Organism (PEP-001)
                  ├─ scores via ──────────► Judge (PEP-002)
                  ├─ emits to ────────────► Event Log (PEP-004)
                  ├─ imports/exports via ─► Sharing (PEP-005)
                  └─ enforces ────────────► Privacy (PEP-006)
```

## Status

All specifications are in **Draft** status. Schemas and stubs track the draft. Breaking changes are versioned in `pyproject.toml`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome — all contributions are licensed under MIT.

## License

[MIT](LICENSE) — Copyright 2026 TechKnowMad AI

---

Built by [TechKnowMad Labs](https://techknowmad.ai)
