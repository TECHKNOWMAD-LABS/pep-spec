"""PEP-005 Sharing conformance tests — 18 tests."""

from __future__ import annotations

import copy
from typing import Any

import jsonschema
import pytest

from conformance.helpers import VALID_CHECKSUM, VALID_DATETIME, VALID_UUID, VALID_UUID_2, VALID_UUID_3, load_schema
from stubs.sharing import (
    Integrity,
    IntegrityAlgorithm,
    Permissions,
    SharingFormat,
    SharingManifest,
    SharingSource,
    TargetProtocol,
)

SCHEMA = load_schema("sharing")


# ── Schema: valid ───────────────────────────────────────────────────────────

def test_valid_sharing_passes_schema(valid_sharing: dict[str, Any]) -> None:
    jsonschema.validate(valid_sharing, SCHEMA)


def test_sharing_all_formats() -> None:
    for fmt in ["pep-native", "onnx", "safetensors", "json", "custom"]:
        doc = {
            "id": VALID_UUID, "format": fmt,
            "source": {"organism_id": VALID_UUID_2, "engine_id": VALID_UUID_3, "generation": 0},
            "target": {"uri": "https://example.com", "protocol": "https"},
            "content": {"genome": True, "phenotype": False, "history": False, "size_bytes": 0},
            "integrity": {"algorithm": "sha256", "hash": VALID_CHECKSUM},
            "permissions": {"public": True, "allowed_consumers": []},
        }
        jsonschema.validate(doc, SCHEMA)


def test_sharing_all_protocols() -> None:
    protos = {"https": "https://x.com", "ipfs": "ipfs://Qm123", "s3": "s3://bucket/key", "local": "file:///tmp/x"}
    for proto, uri in protos.items():
        doc = {
            "id": VALID_UUID, "format": "json",
            "source": {"organism_id": VALID_UUID_2, "engine_id": VALID_UUID_3, "generation": 0},
            "target": {"uri": uri, "protocol": proto},
            "content": {"genome": True, "phenotype": False, "history": False, "size_bytes": 0},
            "integrity": {"algorithm": "sha256", "hash": "a" * 64},
            "permissions": {"public": True, "allowed_consumers": []},
        }
        jsonschema.validate(doc, SCHEMA)


def test_sharing_with_expires_at(valid_sharing: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_sharing)
    doc["permissions"]["expires_at"] = VALID_DATETIME
    jsonschema.validate(doc, SCHEMA)


def test_sharing_with_signature(valid_sharing: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_sharing)
    doc["integrity"]["signature"] = "sig123"
    jsonschema.validate(doc, SCHEMA)


# ── Schema: invalid ─────────────────────────────────────────────────────────

def test_sharing_invalid_format(valid_sharing: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_sharing)
    doc["format"] = "parquet"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_sharing_invalid_protocol(valid_sharing: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_sharing)
    doc["target"]["protocol"] = "ftp"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_sharing_negative_size_bytes(valid_sharing: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_sharing)
    doc["content"]["size_bytes"] = -1
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_sharing_invalid_algorithm(valid_sharing: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_sharing)
    doc["integrity"]["algorithm"] = "md5"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_sharing_missing_source(valid_sharing: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_sharing)
    del doc["source"]
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_sharing_additional_properties(valid_sharing: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_sharing)
    doc["bonus"] = True
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


def test_sharing_empty_hash(valid_sharing: dict[str, Any]) -> None:
    doc = copy.deepcopy(valid_sharing)
    doc["integrity"]["hash"] = ""
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(doc, SCHEMA)


# ── Stub tests ──────────────────────────────────────────────────────────────

def test_sharing_stub_from_dict(valid_sharing: dict[str, Any]) -> None:
    m = SharingManifest.from_dict(valid_sharing)
    assert m.format == SharingFormat.PEP_NATIVE
    assert m.content.size_bytes == 102400


def test_sharing_stub_roundtrip(valid_sharing: dict[str, Any]) -> None:
    m = SharingManifest.from_dict(valid_sharing)
    assert m.to_dict() == valid_sharing


def test_sharing_integrity_with_signature() -> None:
    i = Integrity(algorithm=IntegrityAlgorithm.SHA512, hash="abc", signature="sig")
    d = i.to_dict()
    assert d["signature"] == "sig"
    rt = Integrity.from_dict(d)
    assert rt.signature == "sig"


def test_sharing_permissions_expires() -> None:
    p = Permissions(public=True, allowed_consumers=[], expires_at=VALID_DATETIME)
    d = p.to_dict()
    assert d["expires_at"] == VALID_DATETIME


def test_sharing_format_enum() -> None:
    assert SharingFormat.ONNX.value == "onnx"
    assert TargetProtocol.IPFS.value == "ipfs"


def test_sharing_source_roundtrip() -> None:
    s = SharingSource(organism_id=VALID_UUID, engine_id=VALID_UUID_2, generation=10)
    rt = SharingSource.from_dict(s.to_dict())
    assert rt.generation == 10
