# PEP -- Protocol for Evolutionary Programs

A formal specification for an AI agent ecosystem built around evolutionary computation. PEP defines seven interoperating components that together enable reproducible, observable, and privacy-aware evolutionary processes.

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

## Directory Structure

```
pep-spec/
  specs/           # Markdown specification documents (PEP-001 through PEP-007)
  schemas/         # JSON Schema (draft 2020-12) for each spec
  types/           # TypeScript type definitions
  stubs/           # Python dataclass stubs with from_dict/to_dict
  conformance/     # 125 pytest conformance tests
  README.md
  LICENSE          # MIT
  pyproject.toml
```

## Quick Start

### Install dependencies

```bash
pip install jsonschema pytest
```

### Run conformance tests

```bash
pytest conformance/ -v
```

All 125 tests validate JSON Schema conformance, Python stub serialization round-trips, edge cases, and cross-spec references.

### Use the Python stubs

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
assert org.to_dict() == data
```

### Validate against JSON Schema

```python
import json
import jsonschema

with open("schemas/organism.schema.json") as f:
    schema = json.load(f)

jsonschema.validate(data, schema)  # raises on invalid
```

## Status

All specifications are in **Draft** status. Feedback and contributions welcome.

## License

[MIT](LICENSE) -- Copyright 2026 TechKnowmad AI
