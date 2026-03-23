# Changelog

All notable changes to the PEP (Protocol for Evolutionary Programs) specification.

## [0.1.0] — 2026-03-23

### Added
- **Cycle 1 — Test Coverage**: 58 new tests (44 edge-case + 14 integration), achieving 100% stub coverage (536/536 statements)
- **Cycle 2 — Error Hardening**: `ValidationError` with field-level messages for all 7 stubs; UUID, semver, range, enum, string validation
- **Cycle 3 — Performance**: `lru_cache` on schema loading (eliminates redundant I/O); pre-compiled regex patterns in validation
- **Cycle 4 — Security**: CWE-22 path traversal prevention in `load_schema`; scan confirmed 0 hardcoded secrets, 0 injection vectors
- **Cycle 5 — CI/CD**: GitHub Actions workflow (Python 3.12, ruff, pytest, coverage gate); pre-commit config (ruff + mypy); `.gitignore`
- **Cycle 6 — Property-Based Testing**: 10 Hypothesis tests across all 7 modules with 380+ generated examples; found semver edge case
- **Cycle 7 — Examples + Docs**: 3 working examples (`create_organism`, `evolution_pipeline`, `schema_validation`); docstrings on all 35+ public classes
- **Cycle 8 — Release Engineering**: `CHANGELOG.md`, `Makefile`, `AGENTS.md`, `EVOLUTION.md`, pyproject.toml updates, v0.1.0 tag

### Foundation (pre-Edgecraft)
- 7 PEP specifications (PEP-001 through PEP-007)
- 7 JSON Schema files (draft 2020-12)
- 7 Python stub modules with `from_dict`/`to_dict` serialization
- TypeScript type definitions
- 125 conformance tests
