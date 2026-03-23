"""Cross-module integration tests for PEP spec stubs."""

from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from conformance.helpers import VALID_UUID, VALID_UUID_2, VALID_UUID_3, VALID_CHECKSUM, VALID_DATETIME

from stubs.organism import Organism, OrganismStatus
from stubs.judge import Judge, Verdict, VerdictDetail, Criterion, Metric, JudgeConfig
from stubs.engine import Engine, Population, Selection, Crossover, EngineMutation, Termination, SelectionStrategy, CrossoverMethod
from stubs.event_log import EventLog, EventSource, EventType, ComponentType
from stubs.sharing import SharingManifest, SharingFormat, TargetProtocol, IntegrityAlgorithm
from stubs.privacy import PrivacyPolicy, PrivacyScope, Retention, Consent, Audit, PrivacyRule, RuleAction, RuleCondition, ConditionContext
from stubs.agent import Agent, AgentRole, AgentStatus, AgentBindings, AgentPolicy, AgentState


# ── Cross-module integration ─────────────────────────────────────────────


class TestOrganismJudgeIntegration:
    """Verify that organism IDs flow correctly into judge verdicts."""

    def test_verdict_references_organism_id(self, valid_organism: dict, valid_judge: dict) -> None:
        organism = Organism.from_dict(valid_organism)
        valid_judge["verdict"]["organism_id"] = organism.id
        judge = Judge.from_dict(valid_judge)
        assert judge.verdict.organism_id == organism.id

    def test_judge_evaluates_multiple_criteria(self, valid_judge: dict) -> None:
        judge = Judge.from_dict(valid_judge)
        assert len(judge.criteria) == 2
        assert all(0.0 <= c.weight <= 1.0 for c in judge.criteria)


class TestEnginePopulationIntegration:
    """Verify engine population tracks organism IDs."""

    def test_population_contains_organism_ids(self, valid_engine: dict, valid_organism: dict) -> None:
        organism = Organism.from_dict(valid_organism)
        valid_engine["population"]["organisms"] = [organism.id]
        engine = Engine.from_dict(valid_engine)
        assert organism.id in engine.population.organisms

    def test_engine_roundtrip_preserves_all_nested(self, valid_engine: dict) -> None:
        engine = Engine.from_dict(valid_engine)
        roundtrip = Engine.from_dict(engine.to_dict())
        assert roundtrip.to_dict() == engine.to_dict()


class TestEventLogSourceIntegration:
    """Verify event logs reference correct component types."""

    def test_event_log_from_engine(self, valid_event_log: dict) -> None:
        event = EventLog.from_dict(valid_event_log)
        assert event.source.component == ComponentType.ENGINE
        assert event.type == EventType.ORGANISM_CREATED

    def test_event_log_all_component_sources(self) -> None:
        for comp in ComponentType:
            source = EventSource(component=comp, id=VALID_UUID)
            d = source.to_dict()
            restored = EventSource.from_dict(d)
            assert restored.component == comp


class TestSharingPrivacyIntegration:
    """Verify sharing manifests and privacy policies can coexist on same organism."""

    def test_sharing_and_privacy_same_organism(self, valid_sharing: dict, valid_privacy: dict) -> None:
        manifest = SharingManifest.from_dict(valid_sharing)
        policy = PrivacyPolicy.from_dict(valid_privacy)
        # Both reference organism scope / organism_id
        assert manifest.source.organism_id == VALID_UUID_2
        assert policy.scope == PrivacyScope.ORGANISM

    def test_privacy_retention_with_archive(self, valid_privacy: dict) -> None:
        """Exercises the archive_after_days branch (privacy.py line 86)."""
        valid_privacy["retention"]["archive_after_days"] = 90
        policy = PrivacyPolicy.from_dict(valid_privacy)
        d = policy.to_dict()
        assert d["retention"]["archive_after_days"] == 90
        # Roundtrip
        restored = PrivacyPolicy.from_dict(d)
        assert restored.retention.archive_after_days == 90


class TestAgentBindingsIntegration:
    """Verify agent bindings reference correct entity IDs."""

    def test_agent_binds_to_organism_and_engine(self, valid_agent: dict) -> None:
        agent = Agent.from_dict(valid_agent)
        assert VALID_UUID_3 in agent.bindings.organism_ids
        assert agent.bindings.engine_id == VALID_UUID_2

    def test_agent_without_engine_binding(self) -> None:
        bindings = AgentBindings(organism_ids=[VALID_UUID], judge_ids=[])
        d = bindings.to_dict()
        assert "engine_id" not in d
        restored = AgentBindings.from_dict({**d, "organism_ids": [VALID_UUID], "judge_ids": []})
        assert restored.engine_id is None


class TestFullPipelineIntegration:
    """End-to-end: create organism -> evaluate -> log event -> share."""

    def test_full_pipeline_roundtrip(
        self,
        valid_organism: dict,
        valid_judge: dict,
        valid_event_log: dict,
        valid_sharing: dict,
    ) -> None:
        # Step 1: Create organism
        organism = Organism.from_dict(valid_organism)
        assert organism.status == OrganismStatus.ALIVE

        # Step 2: Judge evaluates organism
        valid_judge["verdict"]["organism_id"] = organism.id
        judge = Judge.from_dict(valid_judge)
        assert judge.verdict.organism_id == organism.id
        assert judge.verdict.passed is True

        # Step 3: Log the evaluation event
        valid_event_log["type"] = "organism.evaluated"
        valid_event_log["payload"] = {"organism_id": organism.id, "score": judge.verdict.score}
        event = EventLog.from_dict(valid_event_log)
        assert event.type == EventType.ORGANISM_EVALUATED

        # Step 4: Share the organism
        valid_sharing["source"]["organism_id"] = organism.id
        manifest = SharingManifest.from_dict(valid_sharing)
        assert manifest.source.organism_id == organism.id


class TestDeepCopyIndependence:
    """Verify that from_dict creates independent objects (no shared references)."""

    def test_organism_copy_independence(self, valid_organism: dict) -> None:
        o1 = Organism.from_dict(valid_organism)
        data2 = copy.deepcopy(valid_organism)
        data2["name"] = "different"
        o2 = Organism.from_dict(data2)
        assert o1.name != o2.name

    def test_engine_copy_independence(self, valid_engine: dict) -> None:
        e1 = Engine.from_dict(valid_engine)
        data2 = copy.deepcopy(valid_engine)
        data2["population"]["size"] = 999
        e2 = Engine.from_dict(data2)
        assert e1.population.size != e2.population.size
