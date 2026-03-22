"""PEP-007 Agent — autonomous actor in the PEP ecosystem."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar


class AgentRole(str, Enum):
    EVOLVER = "evolver"
    GUARDIAN = "guardian"
    EXPLORER = "explorer"
    HARVESTER = "harvester"
    ORCHESTRATOR = "orchestrator"


class AgentStatus(str, Enum):
    IDLE = "idle"
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"


@dataclass
class AgentBindings:
    organism_ids: list[str] = field(default_factory=list)
    judge_ids: list[str] = field(default_factory=list)
    engine_id: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentBindings:
        return cls(
            organism_ids=data["organism_ids"],
            judge_ids=data["judge_ids"],
            engine_id=data.get("engine_id"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "organism_ids": self.organism_ids,
            "judge_ids": self.judge_ids,
        }
        if self.engine_id is not None:
            result["engine_id"] = self.engine_id
        return result


@dataclass
class AgentPolicy:
    max_actions_per_minute: int
    require_approval: bool
    allowed_actions: list[str] = field(default_factory=list)
    denied_actions: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentPolicy:
        return cls(
            max_actions_per_minute=data["max_actions_per_minute"],
            require_approval=data["require_approval"],
            allowed_actions=data["allowed_actions"],
            denied_actions=data["denied_actions"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "max_actions_per_minute": self.max_actions_per_minute,
            "require_approval": self.require_approval,
            "allowed_actions": self.allowed_actions,
            "denied_actions": self.denied_actions,
        }


@dataclass
class AgentState:
    status: AgentStatus
    error_count: int = 0
    current_task: str | None = None
    last_action_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AgentState:
        return cls(
            status=AgentStatus(data["status"]),
            error_count=data["error_count"],
            current_task=data.get("current_task"),
            last_action_at=data.get("last_action_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "status": self.status.value,
            "error_count": self.error_count,
        }
        if self.current_task is not None:
            result["current_task"] = self.current_task
        if self.last_action_at is not None:
            result["last_action_at"] = self.last_action_at
        return result


@dataclass
class Agent:
    id: str
    name: str
    version: str
    role: AgentRole
    capabilities: list[str]
    bindings: AgentBindings
    policy: AgentPolicy
    state: AgentState

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Agent:
        return cls(
            id=data["id"],
            name=data["name"],
            version=data["version"],
            role=AgentRole(data["role"]),
            capabilities=data["capabilities"],
            bindings=AgentBindings.from_dict(data["bindings"]),
            policy=AgentPolicy.from_dict(data["policy"]),
            state=AgentState.from_dict(data["state"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "version": self.version,
            "role": self.role.value,
            "capabilities": self.capabilities,
            "bindings": self.bindings.to_dict(),
            "policy": self.policy.to_dict(),
            "state": self.state.to_dict(),
        }
