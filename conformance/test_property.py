"""Property-based tests using Hypothesis — invariant verification."""

from __future__ import annotations

import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from stubs.agent import (
    Agent,
    AgentBindings,
    AgentPolicy,
    AgentRole,
    AgentState,
    AgentStatus,
)
from stubs.engine import (
    Crossover,
    CrossoverMethod,
    Engine,
    EngineMutation,
    Population,
    Selection,
    SelectionStrategy,
    Termination,
)
from stubs.event_log import ComponentType, EventLog, EventSource, EventType
from stubs.judge import Metric, VerdictDetail
from stubs.organism import (
    Genome,
    Organism,
    OrganismMetadata,
    OrganismStatus,
    Phenotype,
    Trait,
)
from stubs.privacy import (
    Audit,
    Consent,
    PrivacyPolicy,
    PrivacyRule,
    PrivacyScope,
    Retention,
    RuleAction,
)
from stubs.sharing import (
    Integrity,
    IntegrityAlgorithm,
    Permissions,
    SharingContent,
    SharingFormat,
    SharingManifest,
    SharingSource,
    SharingTarget,
    TargetProtocol,
)
from stubs.validation import ValidationError

# ── Strategies ───────────────────────────────────────────────────────────

uuid_st = st.from_regex(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    fullmatch=True,
)
semver_st = st.builds(
    lambda major, minor, patch: f"{major}.{minor}.{patch}",
    st.integers(min_value=0, max_value=999),
    st.integers(min_value=0, max_value=999),
    st.integers(min_value=0, max_value=999),
)
datetime_st = st.from_regex(
    r"20[2-3][0-9]-[0-1][0-9]-[0-3][0-9]T[0-2][0-9]:[0-5][0-9]:[0-5][0-9]Z",
    fullmatch=True,
)
weight_st = st.floats(min_value=0.0, max_value=1.0, allow_nan=False)
name_st = st.text(
    alphabet=st.characters(whitelist_categories=("L", "N", "Pd")),
    min_size=1, max_size=64,
)
checksum_st = st.from_regex(r"[0-9a-f]{64}", fullmatch=True)


# ── Organism roundtrip ───────────────────────────────────────────────────


@given(
    name=name_st,
    weight=weight_st,
    value=st.integers(min_value=-1000, max_value=1000),
)
@settings(max_examples=50)
def test_trait_roundtrip(name: str, weight: float, value: int) -> None:
    t = Trait(name=name, value=value, weight=weight)
    d = t.to_dict()
    restored = Trait.from_dict(d)
    assert restored.name == name
    assert restored.value == value
    assert restored.weight == weight


@given(
    uuid=uuid_st,
    name=name_st,
    version=semver_st,
    status=st.sampled_from([s.value for s in OrganismStatus]),
    n_traits=st.integers(min_value=0, max_value=5),
)
@settings(max_examples=30)
def test_organism_roundtrip_property(
    uuid: str, name: str, version: str, status: str, n_traits: int,
) -> None:
    traits = [Trait(name=f"t{i}", value=i, weight=0.5) for i in range(n_traits)]
    genome = Genome(traits=traits, mutations=[])
    phenotype = Phenotype(capabilities=[], constraints=[])
    metadata = OrganismMetadata(
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )
    org = Organism(
        id=uuid, name=name, version=version,
        genome=genome, phenotype=phenotype,
        metadata=metadata, status=OrganismStatus(status),
    )
    d = org.to_dict()
    restored = Organism.from_dict(d)
    assert restored.to_dict() == d


# ── Judge roundtrip ──────────────────────────────────────────────────────


@given(
    score=weight_st,
    passed=st.booleans(),
    metric=st.sampled_from([m.value for m in Metric]),
)
@settings(max_examples=30)
def test_judge_verdict_roundtrip(score: float, passed: bool, metric: str) -> None:
    detail = VerdictDetail(criterion="test", score=score, passed=passed)
    d = detail.to_dict()
    restored = VerdictDetail.from_dict(d)
    assert restored.score == score
    assert restored.passed == passed


# ── Engine roundtrip ─────────────────────────────────────────────────────


@given(
    strategy=st.sampled_from([s.value for s in SelectionStrategy]),
    method=st.sampled_from([m.value for m in CrossoverMethod]),
    pressure=weight_st,
    rate=weight_st,
    mutation_rate=weight_st,
    decay=weight_st,
    pop_size=st.integers(min_value=1, max_value=10000),
)
@settings(max_examples=30)
def test_engine_roundtrip_property(
    strategy: str, method: str, pressure: float, rate: float,
    mutation_rate: float, decay: float, pop_size: int,
) -> None:
    engine = Engine(
        id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        name="test", version="1.0.0",
        population=Population(size=pop_size, organisms=[], generation=0),
        selection=Selection(
            strategy=SelectionStrategy(strategy),
            pressure=pressure, elitism_rate=0.1,
        ),
        crossover=Crossover(method=CrossoverMethod(method), rate=rate),
        mutation=EngineMutation(rate=mutation_rate, decay=decay),
        termination=Termination(
            max_generations=100, fitness_target=0.9, stagnation_limit=10,
        ),
    )
    d = engine.to_dict()
    restored = Engine.from_dict(d)
    assert restored.to_dict() == d


# ── Event Log roundtrip ──────────────────────────────────────────────────


@given(
    event_type=st.sampled_from([e.value for e in EventType]),
    component=st.sampled_from([c.value for c in ComponentType]),
    sequence=st.integers(min_value=0, max_value=1000000),
)
@settings(max_examples=30)
def test_event_log_roundtrip_property(
    event_type: str, component: str, sequence: int,
) -> None:
    event = EventLog(
        id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        timestamp="2026-01-01T00:00:00Z",
        type=EventType(event_type),
        source=EventSource(component=ComponentType(component), id="b2c3d4e5-f6a7-8901-bcde-f12345678901"),
        payload={"test": True},
        sequence=sequence,
        checksum="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    )
    d = event.to_dict()
    restored = EventLog.from_dict(d)
    assert restored.to_dict() == d


# ── Sharing roundtrip ────────────────────────────────────────────────────


@given(
    fmt=st.sampled_from([f.value for f in SharingFormat]),
    protocol=st.sampled_from([p.value for p in TargetProtocol]),
    algo=st.sampled_from([a.value for a in IntegrityAlgorithm]),
    public=st.booleans(),
    size=st.integers(min_value=0, max_value=1000000),
)
@settings(max_examples=30)
def test_sharing_roundtrip_property(
    fmt: str, protocol: str, algo: str, public: bool, size: int,
) -> None:
    manifest = SharingManifest(
        id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        format=SharingFormat(fmt),
        source=SharingSource(
            organism_id="b2c3d4e5-f6a7-8901-bcde-f12345678901",
            engine_id="c3d4e5f6-a7b8-9012-cdef-123456789012",
            generation=0,
        ),
        target=SharingTarget(uri="https://example.com", protocol=TargetProtocol(protocol)),
        content=SharingContent(genome=True, phenotype=False, history=False, size_bytes=size),
        integrity=Integrity(algorithm=IntegrityAlgorithm(algo), hash="abc123"),
        permissions=Permissions(public=public),
    )
    d = manifest.to_dict()
    restored = SharingManifest.from_dict(d)
    assert restored.to_dict() == d


# ── Privacy roundtrip ────────────────────────────────────────────────────


@given(
    scope=st.sampled_from([s.value for s in PrivacyScope]),
    action=st.sampled_from([a.value for a in RuleAction]),
    max_age=st.integers(min_value=1, max_value=3650),
    auto_purge=st.booleans(),
)
@settings(max_examples=30)
def test_privacy_roundtrip_property(
    scope: str, action: str, max_age: int, auto_purge: bool,
) -> None:
    policy = PrivacyPolicy(
        id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        version="1.0.0",
        scope=PrivacyScope(scope),
        rules=[PrivacyRule(field="test.field", action=RuleAction(action))],
        retention=Retention(max_age_days=max_age, auto_purge=auto_purge),
        consent=Consent(required=False),
        audit=Audit(log_access=True, log_mutations=True, require_justification=False),
    )
    d = policy.to_dict()
    restored = PrivacyPolicy.from_dict(d)
    assert restored.to_dict() == d


# ── Agent roundtrip ──────────────────────────────────────────────────────


@given(
    role=st.sampled_from([r.value for r in AgentRole]),
    status=st.sampled_from([s.value for s in AgentStatus]),
    max_actions=st.integers(min_value=1, max_value=1000),
    error_count=st.integers(min_value=0, max_value=100),
)
@settings(max_examples=30)
def test_agent_roundtrip_property(
    role: str, status: str, max_actions: int, error_count: int,
) -> None:
    agent = Agent(
        id="a1b2c3d4-e5f6-7890-abcd-ef1234567890",
        name="test-agent", version="1.0.0",
        role=AgentRole(role),
        capabilities=["test"],
        bindings=AgentBindings(organism_ids=[], judge_ids=[]),
        policy=AgentPolicy(
            max_actions_per_minute=max_actions,
            require_approval=False,
        ),
        state=AgentState(status=AgentStatus(status), error_count=error_count),
    )
    d = agent.to_dict()
    restored = Agent.from_dict(d)
    assert restored.to_dict() == d


# ── Validation rejects invalid input (no crashes) ───────────────────────


@given(bad_uuid=st.text(min_size=0, max_size=100))
@settings(max_examples=50)
def test_organism_rejects_invalid_uuid_no_crash(bad_uuid: str) -> None:
    """Organism.from_dict never crashes — it raises ValidationError or succeeds."""
    data = {
        "id": bad_uuid, "name": "x", "version": "1.0.0",
        "status": "alive",
        "genome": {"traits": [], "mutations": []},
        "phenotype": {"capabilities": [], "constraints": []},
        "metadata": {
            "created_at": "2026-01-01T00:00:00Z",
            "updated_at": "2026-01-01T00:00:00Z",
            "tags": [], "lineage": [],
        },
    }
    try:
        Organism.from_dict(data)
    except ValidationError:
        pass  # Expected for invalid UUIDs


@given(weight=st.floats(allow_nan=True, allow_infinity=True))
@settings(max_examples=50)
def test_trait_weight_never_crashes(weight: float) -> None:
    """Trait.from_dict never crashes — it raises ValidationError or succeeds."""
    try:
        Trait.from_dict({"name": "x", "value": 0, "weight": weight})
    except (ValidationError, ValueError):
        pass  # Expected for out-of-range or NaN
