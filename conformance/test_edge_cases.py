"""Edge-case tests for PEP spec stubs — boundary values, optional fields, enums."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from conformance.helpers import VALID_CHECKSUM, VALID_DATETIME, VALID_UUID, VALID_UUID_2
from stubs.agent import AgentBindings, AgentPolicy, AgentRole, AgentState, AgentStatus
from stubs.engine import (
    Crossover,
    CrossoverMethod,
    EngineMutation,
    Population,
    Selection,
    SelectionStrategy,
    Termination,
)
from stubs.event_log import ComponentType, EventLog, EventSource, EventType
from stubs.judge import Criterion, JudgeConfig, Metric, Verdict, VerdictDetail
from stubs.organism import Constraint, Genome, Mutation, OrganismMetadata, OrganismStatus, Phenotype, Trait
from stubs.privacy import (
    ConditionContext,
    Consent,
    PrivacyPolicy,
    PrivacyRule,
    PrivacyScope,
    Retention,
    RuleAction,
    RuleCondition,
)
from stubs.sharing import Integrity, IntegrityAlgorithm, Permissions, SharingContent, SharingFormat, TargetProtocol

# ── Organism edge cases ──────────────────────────────────────────────────


class TestOrganismEdgeCases:
    def test_trait_zero_weight(self) -> None:
        t = Trait(name="x", value=0, weight=0.0)
        assert t.to_dict()["weight"] == 0.0

    def test_trait_max_weight(self) -> None:
        t = Trait(name="x", value=0, weight=1.0)
        assert t.to_dict()["weight"] == 1.0

    def test_mutation_all_operations(self) -> None:
        for op in ("add", "remove", "modify"):
            m = Mutation(gene="g", operation=op, payload=None)
            assert m.to_dict()["operation"] == op

    def test_genome_empty_traits_and_mutations(self) -> None:
        g = Genome()
        d = g.to_dict()
        assert d == {"traits": [], "mutations": []}

    def test_organism_metadata_empty_lineage(self) -> None:
        meta = OrganismMetadata(created_at=VALID_DATETIME, updated_at=VALID_DATETIME)
        d = meta.to_dict()
        assert d["lineage"] == []
        assert d["tags"] == []

    def test_phenotype_empty_capabilities(self) -> None:
        p = Phenotype()
        d = p.to_dict()
        assert d == {"capabilities": [], "constraints": []}

    def test_organism_all_statuses_roundtrip(self) -> None:
        for status in OrganismStatus:
            assert OrganismStatus(status.value) == status

    def test_constraint_zero_limit(self) -> None:
        c = Constraint(resource="cpu", limit=0.0)
        assert c.to_dict()["limit"] == 0.0

    def test_mutation_none_payload(self) -> None:
        m = Mutation(gene="x", operation="add", payload=None)
        d = m.to_dict()
        assert d["payload"] is None
        restored = Mutation.from_dict(d)
        assert restored.payload is None

    def test_trait_complex_value(self) -> None:
        t = Trait(name="nested", value={"a": [1, 2, 3]}, weight=0.5)
        d = t.to_dict()
        assert d["value"]["a"] == [1, 2, 3]
        restored = Trait.from_dict(d)
        assert restored.value == {"a": [1, 2, 3]}


# ── Judge edge cases ─────────────────────────────────────────────────────


class TestJudgeEdgeCases:
    def test_all_metrics(self) -> None:
        for m in Metric:
            c = Criterion(name=m.value, weight=0.5, threshold=0.5, metric=m)
            assert c.to_dict()["metric"] == m.value

    def test_verdict_empty_details(self) -> None:
        v = Verdict(organism_id=VALID_UUID, score=0.0, passed=False)
        d = v.to_dict()
        assert d["details"] == []

    def test_verdict_detail_boundary_scores(self) -> None:
        for score in (0.0, 0.5, 1.0):
            vd = VerdictDetail(criterion="test", score=score, passed=score >= 0.5)
            assert vd.to_dict()["score"] == score

    def test_judge_config_zero_retries(self) -> None:
        config = JudgeConfig(max_retries=0, timeout_ms=1, parallel=False)
        d = config.to_dict()
        assert d["max_retries"] == 0


# ── Engine edge cases ────────────────────────────────────────────────────


class TestEngineEdgeCases:
    def test_population_single_organism(self) -> None:
        p = Population(size=1, organisms=[VALID_UUID], generation=0)
        d = p.to_dict()
        assert d["size"] == 1

    def test_all_selection_strategies(self) -> None:
        for s in SelectionStrategy:
            sel = Selection(strategy=s, pressure=0.5, elitism_rate=0.1)
            assert sel.to_dict()["strategy"] == s.value

    def test_all_crossover_methods(self) -> None:
        for m in CrossoverMethod:
            c = Crossover(method=m, rate=0.5)
            assert c.to_dict()["method"] == m.value

    def test_mutation_zero_rates(self) -> None:
        m = EngineMutation(rate=0.0, decay=0.0)
        d = m.to_dict()
        assert d["rate"] == 0.0 and d["decay"] == 0.0

    def test_termination_boundary_values(self) -> None:
        t = Termination(max_generations=1, fitness_target=0.0, stagnation_limit=1)
        d = t.to_dict()
        assert d["max_generations"] == 1


# ── Event Log edge cases ─────────────────────────────────────────────────


class TestEventLogEdgeCases:
    def test_all_event_types(self) -> None:
        for et in EventType:
            assert EventType(et.value) == et

    def test_all_component_types(self) -> None:
        for ct in ComponentType:
            assert ComponentType(ct.value) == ct

    def test_event_log_with_correlation_id(self) -> None:
        event = EventLog(
            id=VALID_UUID,
            timestamp=VALID_DATETIME,
            type=EventType.AGENT_ACTION,
            source=EventSource(component=ComponentType.AGENT, id=VALID_UUID_2),
            payload={"action": "test"},
            sequence=42,
            checksum=VALID_CHECKSUM,
            correlation_id=VALID_UUID_2,
        )
        d = event.to_dict()
        assert d["correlation_id"] == VALID_UUID_2

    def test_event_log_without_correlation_id(self) -> None:
        event = EventLog(
            id=VALID_UUID,
            timestamp=VALID_DATETIME,
            type=EventType.ENGINE_STARTED,
            source=EventSource(component=ComponentType.ENGINE, id=VALID_UUID),
            payload={},
            sequence=0,
            checksum=VALID_CHECKSUM,
        )
        d = event.to_dict()
        assert "correlation_id" not in d

    def test_event_log_empty_payload(self) -> None:
        event = EventLog(
            id=VALID_UUID,
            timestamp=VALID_DATETIME,
            type=EventType.ENGINE_STOPPED,
            source=EventSource(component=ComponentType.ENGINE, id=VALID_UUID),
            payload={},
            sequence=0,
            checksum=VALID_CHECKSUM,
        )
        assert event.to_dict()["payload"] == {}


# ── Sharing edge cases ───────────────────────────────────────────────────


class TestSharingEdgeCases:
    def test_all_formats(self) -> None:
        for f in SharingFormat:
            assert SharingFormat(f.value) == f

    def test_all_protocols(self) -> None:
        for p in TargetProtocol:
            assert TargetProtocol(p.value) == p

    def test_all_integrity_algorithms(self) -> None:
        for a in IntegrityAlgorithm:
            assert IntegrityAlgorithm(a.value) == a

    def test_integrity_without_signature(self) -> None:
        i = Integrity(algorithm=IntegrityAlgorithm.BLAKE3, hash="abc123")
        d = i.to_dict()
        assert "signature" not in d

    def test_permissions_no_consumers(self) -> None:
        p = Permissions(public=True)
        d = p.to_dict()
        assert d["allowed_consumers"] == []
        assert "expires_at" not in d

    def test_sharing_content_zero_size(self) -> None:
        c = SharingContent(genome=False, phenotype=False, history=False, size_bytes=0)
        assert c.to_dict()["size_bytes"] == 0


# ── Privacy edge cases ───────────────────────────────────────────────────


class TestPrivacyEdgeCases:
    def test_all_scopes(self) -> None:
        for s in PrivacyScope:
            assert PrivacyScope(s.value) == s

    def test_all_rule_actions(self) -> None:
        for a in RuleAction:
            assert RuleAction(a.value) == a

    def test_all_condition_contexts(self) -> None:
        for c in ConditionContext:
            rc = RuleCondition(context=c)
            assert rc.to_dict()["context"] == c.value

    def test_privacy_rule_without_condition(self) -> None:
        r = PrivacyRule(field="genome", action=RuleAction.HASH)
        d = r.to_dict()
        assert "condition" not in d

    def test_retention_with_archive(self) -> None:
        r = Retention(max_age_days=30, auto_purge=True, archive_after_days=7)
        d = r.to_dict()
        assert d["archive_after_days"] == 7

    def test_retention_without_archive(self) -> None:
        r = Retention(max_age_days=30, auto_purge=False)
        d = r.to_dict()
        assert "archive_after_days" not in d

    def test_consent_minimal(self) -> None:
        c = Consent(required=False)
        d = c.to_dict()
        assert "granted_by" not in d
        assert "granted_at" not in d

    def test_consent_full(self) -> None:
        c = Consent(required=True, granted_by=VALID_UUID, granted_at=VALID_DATETIME)
        d = c.to_dict()
        assert d["granted_by"] == VALID_UUID

    def test_privacy_policy_default_factories(self) -> None:
        policy = PrivacyPolicy(id=VALID_UUID, version="1.0.0", scope=PrivacyScope.GLOBAL)
        assert policy.retention.max_age_days == 365
        assert policy.consent.required is False
        assert policy.audit.log_access is True


# ── Agent edge cases ─────────────────────────────────────────────────────


class TestAgentEdgeCases:
    def test_all_roles(self) -> None:
        for r in AgentRole:
            assert AgentRole(r.value) == r

    def test_all_statuses(self) -> None:
        for s in AgentStatus:
            assert AgentStatus(s.value) == s

    def test_agent_state_minimal(self) -> None:
        state = AgentState(status=AgentStatus.IDLE)
        d = state.to_dict()
        assert d["error_count"] == 0
        assert "current_task" not in d
        assert "last_action_at" not in d

    def test_agent_state_full(self) -> None:
        state = AgentState(
            status=AgentStatus.ACTIVE,
            error_count=5,
            current_task="testing",
            last_action_at=VALID_DATETIME,
        )
        d = state.to_dict()
        assert d["current_task"] == "testing"
        assert d["last_action_at"] == VALID_DATETIME

    def test_agent_bindings_no_engine(self) -> None:
        b = AgentBindings(organism_ids=[], judge_ids=[])
        d = b.to_dict()
        assert "engine_id" not in d

    def test_agent_policy_empty_actions(self) -> None:
        p = AgentPolicy(max_actions_per_minute=1, require_approval=True)
        d = p.to_dict()
        assert d["allowed_actions"] == []
        assert d["denied_actions"] == []
