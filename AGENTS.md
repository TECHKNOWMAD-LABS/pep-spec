# AGENTS.md — Autonomous Development Protocol

This document describes the autonomous development protocol used to improve
the PEP (Protocol for Evolutionary Programs) specification repository.

## Protocol: Edgecraft

Edgecraft is an autonomous iterative development protocol where each cycle
performs a complete L0-L7 pass over the codebase:

| Layer | Name | Purpose |
|-------|------|---------|
| L0 | Attention | Identify what matters in the codebase |
| L1 | Detection | Find untested, uncovered, or broken modules |
| L2 | Noise | Scan for security issues, distinguish signal from noise |
| L3 | Sub-noise | Find subtle bugs, edge cases, and hidden failures |
| L4 | Conjecture | Hypothesize improvements (perf, reliability, security) |
| L5 | Action | Implement fixes, tests, features, and infrastructure |
| L6 | Grounding | Verify with measurements (test counts, coverage, timing) |
| L7 | Flywheel | Identify patterns reusable across other repositories |

## Cycles Executed

8 complete cycles were executed on 2026-03-23:

1. **Test Coverage** — Identified 1% uncovered code, added 58 edge-case and integration tests, achieved 100% coverage
2. **Error Hardening** — Added `ValidationError` with field-level messages to all 7 stubs
3. **Performance** — Added `lru_cache` for schema loading, pre-compiled regex
4. **Security** — Fixed CWE-22 path traversal, confirmed 0 secrets/injection vectors
5. **CI/CD** — GitHub Actions, pre-commit hooks, ruff configuration
6. **Property-Based Testing** — Hypothesis tests found semver edge case
7. **Examples + Docs** — 3 working examples, docstrings on all public classes
8. **Release Engineering** — CHANGELOG, Makefile, pyproject.toml, v0.1.0 tag

## Commit Convention

Every commit message starts with an Edgecraft layer prefix:

```
L0/attention:  — observation or awareness
L1/detection:  — finding something broken/untested
L2/noise:      — security scan results
L3/sub-noise:  — subtle edge case or hidden bug
L4/conjecture: — hypothesis about improvement
L5/action:     — implementation of fix/feature
L6/grounding:  — verification with measurements
L7/flywheel:   — reusable pattern identification
```

## Agent Configuration

- **Model**: Claude Opus 4.6
- **Mode**: Fully autonomous (no human approval required)
- **Git identity**: TechKnowMad Labs <admin@techknowmad.ai>
- **Push policy**: Push after each cycle completes
- **Test policy**: Run full test suite after every code change; fix before committing

## Quality Gates

- 100% test coverage (536/536 statements)
- 252 tests passing (125 conformance + 58 edge-case + 14 integration + 10 property + 47 validation + 8 security + 4 performance)
- 0 ruff lint errors
- 0 hardcoded secrets
- All 3 examples verified working
