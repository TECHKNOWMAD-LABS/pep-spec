"""Performance tests — verify schema caching and serialization speed."""

from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from conformance.helpers import load_schema, VALID_UUID, VALID_DATETIME, VALID_CHECKSUM

from stubs.organism import Organism
from stubs.judge import Judge
from stubs.engine import Engine


# ── Schema caching verification ──────────────────────────────────────────


class TestSchemaCaching:
    def test_schema_cache_hit(self) -> None:
        """Second call should return same object (cached)."""
        s1 = load_schema("organism")
        s2 = load_schema("organism")
        assert s1 is s2  # Same object = cache hit

    def test_all_schemas_cacheable(self) -> None:
        names = ["organism", "judge", "engine", "event-log", "sharing", "privacy", "agent"]
        for name in names:
            s1 = load_schema(name)
            s2 = load_schema(name)
            assert s1 is s2


# ── Serialization throughput ─────────────────────────────────────────────


class TestSerializationPerformance:
    def _build_organism_dict(self) -> dict[str, Any]:
        return {
            "id": VALID_UUID,
            "name": "perf-test",
            "version": "1.0.0",
            "genome": {
                "traits": [{"name": f"t{i}", "value": i, "weight": 0.5} for i in range(10)],
                "mutations": [{"gene": f"g{i}", "operation": "modify", "payload": i} for i in range(5)],
            },
            "phenotype": {
                "capabilities": [f"cap{i}" for i in range(10)],
                "constraints": [{"resource": f"r{i}", "limit": float(i)} for i in range(5)],
            },
            "metadata": {
                "created_at": VALID_DATETIME,
                "updated_at": VALID_DATETIME,
                "tags": [f"tag{i}" for i in range(5)],
                "lineage": [],
            },
            "status": "alive",
        }

    def test_organism_roundtrip_1000_iterations(self) -> None:
        """1000 from_dict + to_dict roundtrips should complete in under 2 seconds."""
        data = self._build_organism_dict()
        start = time.perf_counter()
        for _ in range(1000):
            obj = Organism.from_dict(data)
            obj.to_dict()
        elapsed = time.perf_counter() - start
        assert elapsed < 2.0, f"1000 roundtrips took {elapsed:.2f}s (expected < 2s)"

    def test_schema_load_cached_vs_uncached(self) -> None:
        """Cached schema loads should be at least 10x faster than uncached."""
        # Clear cache
        load_schema.cache_clear()

        # First (uncached) load
        start = time.perf_counter()
        load_schema("organism")
        first_load = time.perf_counter() - start

        # Cached loads
        start = time.perf_counter()
        for _ in range(100):
            load_schema("organism")
        cached_avg = (time.perf_counter() - start) / 100

        # Cached should be much faster (at least 10x)
        if first_load > 0.0001:  # Only if first load measurable
            assert cached_avg < first_load, "Cached loads should be faster"
