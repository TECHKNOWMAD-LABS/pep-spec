#!/usr/bin/env python3
"""Example: Simulate a complete evolution pipeline.

Demonstrates the full PEP workflow:
1. Create an Engine with evolutionary parameters
2. Create organisms in the population
3. Judge evaluates organisms
4. Log events to the audit trail
5. Privacy policy protects sensitive fields
6. Agent orchestrates the process
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from stubs.organism import (
    Organism, OrganismStatus, Trait, Genome, Phenotype,
    OrganismMetadata,
)
from stubs.judge import (
    Judge, Criterion, Metric, Verdict, VerdictDetail, JudgeConfig,
)
from stubs.engine import (
    Engine, Population, Selection, SelectionStrategy,
    Crossover, CrossoverMethod, EngineMutation, Termination,
)
from stubs.event_log import EventLog, EventSource, EventType, ComponentType
from stubs.privacy import (
    PrivacyPolicy, PrivacyRule, RuleAction, RuleCondition,
    ConditionContext, PrivacyScope, Retention, Consent, Audit,
)
from stubs.agent import (
    Agent, AgentRole, AgentBindings, AgentPolicy, AgentState, AgentStatus,
)


VALID_CHECKSUM = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

ORG_ID = "11111111-1111-1111-1111-111111111111"
ENGINE_ID = "22222222-2222-2222-2222-222222222222"
JUDGE_ID = "33333333-3333-3333-3333-333333333333"
AGENT_ID = "44444444-4444-4444-4444-444444444444"


def main() -> None:
    # ── Step 1: Configure the engine ──────────────────────────────────
    engine = Engine(
        id=ENGINE_ID,
        name="main-evolution-engine",
        version="2.0.0",
        population=Population(size=100, organisms=[ORG_ID], generation=0),
        selection=Selection(
            strategy=SelectionStrategy.TOURNAMENT,
            pressure=0.7,
            elitism_rate=0.1,
        ),
        crossover=Crossover(method=CrossoverMethod.UNIFORM, rate=0.8),
        mutation=EngineMutation(rate=0.05, decay=0.01),
        termination=Termination(
            max_generations=500,
            fitness_target=0.95,
            stagnation_limit=50,
        ),
    )
    print(f"Engine: {engine.name} (pop={engine.population.size})")

    # ── Step 2: Create an organism ────────────────────────────────────
    organism = Organism(
        id=ORG_ID,
        name="alpha-organism",
        version="1.0.0",
        genome=Genome(
            traits=[Trait(name="accuracy", value=0.92, weight=0.8)],
            mutations=[],
        ),
        phenotype=Phenotype(capabilities=["classify", "predict"], constraints=[]),
        metadata=OrganismMetadata(
            created_at="2026-01-15T10:30:00Z",
            updated_at="2026-01-15T10:30:00Z",
            tags=["gen-0"],
            lineage=[],
        ),
        status=OrganismStatus.ALIVE,
    )
    print(f"Organism: {organism.name} ({organism.status.value})")

    # ── Step 3: Judge evaluates ───────────────────────────────────────
    judge = Judge(
        id=JUDGE_ID,
        name="fitness-judge",
        version="1.0.0",
        criteria=[
            Criterion(name="accuracy", weight=0.7, threshold=0.9, metric=Metric.ACCURACY),
            Criterion(name="speed", weight=0.3, threshold=0.5, metric=Metric.LATENCY),
        ],
        verdict=Verdict(
            organism_id=ORG_ID,
            score=0.88,
            passed=True,
            details=[
                VerdictDetail(criterion="accuracy", score=0.92, passed=True),
                VerdictDetail(criterion="speed", score=0.75, passed=True),
            ],
        ),
        config=JudgeConfig(max_retries=3, timeout_ms=5000, parallel=True),
    )
    print(f"Judge verdict: score={judge.verdict.score}, passed={judge.verdict.passed}")

    # ── Step 4: Log the event ─────────────────────────────────────────
    event = EventLog(
        id="55555555-5555-5555-5555-555555555555",
        timestamp="2026-01-15T10:31:00Z",
        type=EventType.ORGANISM_EVALUATED,
        source=EventSource(component=ComponentType.JUDGE, id=JUDGE_ID),
        payload={"organism_id": ORG_ID, "score": 0.88},
        sequence=1,
        checksum=VALID_CHECKSUM,
        correlation_id=ENGINE_ID,
    )
    print(f"Event: {event.type.value} (seq={event.sequence})")

    # ── Step 5: Privacy policy ────────────────────────────────────────
    privacy = PrivacyPolicy(
        id="66666666-6666-6666-6666-666666666666",
        version="1.0.0",
        scope=PrivacyScope.ORGANISM,
        rules=[
            PrivacyRule(
                field="genome.traits",
                action=RuleAction.REDACT,
                condition=RuleCondition(context=ConditionContext.EXPORT),
            ),
        ],
        retention=Retention(max_age_days=365, auto_purge=True),
        consent=Consent(required=True, granted_by=AGENT_ID, granted_at="2026-01-15T10:00:00Z"),
        audit=Audit(log_access=True, log_mutations=True, require_justification=False),
    )
    print(f"Privacy: scope={privacy.scope.value}, rules={len(privacy.rules)}")

    # ── Step 6: Agent orchestrates ────────────────────────────────────
    agent = Agent(
        id=AGENT_ID,
        name="evolution-orchestrator",
        version="1.0.0",
        role=AgentRole.ORCHESTRATOR,
        capabilities=["mutate", "crossover", "select", "evaluate"],
        bindings=AgentBindings(
            organism_ids=[ORG_ID],
            judge_ids=[JUDGE_ID],
            engine_id=ENGINE_ID,
        ),
        policy=AgentPolicy(
            max_actions_per_minute=60,
            require_approval=False,
            allowed_actions=["mutate", "crossover", "evaluate"],
            denied_actions=["terminate"],
        ),
        state=AgentState(
            status=AgentStatus.ACTIVE,
            error_count=0,
            current_task="evolving generation 0",
            last_action_at="2026-01-15T10:31:00Z",
        ),
    )
    print(f"Agent: {agent.name} ({agent.role.value}, {agent.state.status.value})")

    # ── Verify all round-trip ─────────────────────────────────────────
    for name, obj in [
        ("Engine", engine),
        ("Organism", organism),
        ("Judge", judge),
        ("EventLog", event),
        ("Privacy", privacy),
        ("Agent", agent),
    ]:
        d = obj.to_dict()
        restored = type(obj).from_dict(d)
        assert restored.to_dict() == d, f"{name} round-trip failed"
        print(f"[OK] {name} round-trip verified")

    print("\n=== Pipeline complete ===")


if __name__ == "__main__":
    main()
