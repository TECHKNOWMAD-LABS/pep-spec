"""PEP-005 Sharing — import/export protocol."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, TypeVar


class SharingFormat(str, Enum):
    PEP_NATIVE = "pep-native"
    ONNX = "onnx"
    SAFETENSORS = "safetensors"
    JSON = "json"
    CUSTOM = "custom"


class TargetProtocol(str, Enum):
    HTTPS = "https"
    IPFS = "ipfs"
    S3 = "s3"
    LOCAL = "local"


class IntegrityAlgorithm(str, Enum):
    SHA256 = "sha256"
    SHA512 = "sha512"
    BLAKE3 = "blake3"


@dataclass
class SharingSource:
    organism_id: str
    engine_id: str
    generation: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SharingSource:
        return cls(
            organism_id=data["organism_id"],
            engine_id=data["engine_id"],
            generation=data["generation"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "organism_id": self.organism_id,
            "engine_id": self.engine_id,
            "generation": self.generation,
        }


@dataclass
class SharingTarget:
    uri: str
    protocol: TargetProtocol

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SharingTarget:
        return cls(uri=data["uri"], protocol=TargetProtocol(data["protocol"]))

    def to_dict(self) -> dict[str, Any]:
        return {"uri": self.uri, "protocol": self.protocol.value}


@dataclass
class SharingContent:
    genome: bool
    phenotype: bool
    history: bool
    size_bytes: int

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SharingContent:
        return cls(
            genome=data["genome"],
            phenotype=data["phenotype"],
            history=data["history"],
            size_bytes=data["size_bytes"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "genome": self.genome,
            "phenotype": self.phenotype,
            "history": self.history,
            "size_bytes": self.size_bytes,
        }


@dataclass
class Integrity:
    algorithm: IntegrityAlgorithm
    hash: str
    signature: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Integrity:
        return cls(
            algorithm=IntegrityAlgorithm(data["algorithm"]),
            hash=data["hash"],
            signature=data.get("signature"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "algorithm": self.algorithm.value,
            "hash": self.hash,
        }
        if self.signature is not None:
            result["signature"] = self.signature
        return result


@dataclass
class Permissions:
    public: bool
    allowed_consumers: list[str] = field(default_factory=list)
    expires_at: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Permissions:
        return cls(
            public=data["public"],
            allowed_consumers=data["allowed_consumers"],
            expires_at=data.get("expires_at"),
        )

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {
            "public": self.public,
            "allowed_consumers": self.allowed_consumers,
        }
        if self.expires_at is not None:
            result["expires_at"] = self.expires_at
        return result


@dataclass
class SharingManifest:
    id: str
    format: SharingFormat
    source: SharingSource
    target: SharingTarget
    content: SharingContent
    integrity: Integrity
    permissions: Permissions

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SharingManifest:
        return cls(
            id=data["id"],
            format=SharingFormat(data["format"]),
            source=SharingSource.from_dict(data["source"]),
            target=SharingTarget.from_dict(data["target"]),
            content=SharingContent.from_dict(data["content"]),
            integrity=Integrity.from_dict(data["integrity"]),
            permissions=Permissions.from_dict(data["permissions"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "format": self.format.value,
            "source": self.source.to_dict(),
            "target": self.target.to_dict(),
            "content": self.content.to_dict(),
            "integrity": self.integrity.to_dict(),
            "permissions": self.permissions.to_dict(),
        }
