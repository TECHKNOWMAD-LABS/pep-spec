"""PEP-005 Sharing — import/export protocol."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from stubs.validation import (
    require_field,
    validate_enum_value,
    validate_range,
    validate_uuid,
)


class SharingFormat(str, Enum):
    """Export formats: pep-native, onnx, safetensors, json, custom."""

    PEP_NATIVE = "pep-native"
    ONNX = "onnx"
    SAFETENSORS = "safetensors"
    JSON = "json"
    CUSTOM = "custom"


class TargetProtocol(str, Enum):
    """Target protocols: https, ipfs, s3, local."""

    HTTPS = "https"
    IPFS = "ipfs"
    S3 = "s3"
    LOCAL = "local"


class IntegrityAlgorithm(str, Enum):
    """Hash algorithms: sha256, sha512, blake3."""

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
        validate_uuid(require_field(data, "organism_id", str), "organism_id")
        validate_uuid(require_field(data, "engine_id", str), "engine_id")
        validate_range(require_field(data, "generation", int), "generation", min_val=0)
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
        validate_uuid(require_field(data, "id", str), "id")
        validate_enum_value(require_field(data, "format", str), {f.value for f in SharingFormat}, "format")
        require_field(data, "source", dict)
        require_field(data, "target", dict)
        require_field(data, "content", dict)
        require_field(data, "integrity", dict)
        require_field(data, "permissions", dict)
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
