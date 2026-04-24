"""Registry matching and deterministic fingerprints (pure a1)."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.schemas import COMPONENT_SCHEMA_V11, REGISTRY_SNAPSHOT_SCHEMA

_TOKEN_RE = re.compile(r"[^a-z0-9]+", re.IGNORECASE)


def fold_registry_token(value: str) -> str:
    """Alphanumeric fold for registry / dedup ids (shared with ingest + gap-fill)."""
    return _TOKEN_RE.sub("", str(value).lower())


def registry_row_lookup_keys(component: dict[str, Any]) -> list[str]:
    """Candidate folded keys for a registry row (id, name, implementation stem)."""
    keys: list[str] = []
    for field in ("id", "name"):
        raw = component.get(field)
        if raw:
            keys.append(fold_registry_token(str(raw)))
    impl = component.get("_implementation")
    if impl:
        keys.append(fold_registry_token(Path(str(impl)).stem))
    return [k for k in keys if k]


def match_registry_row(symbol_name: str, registry: list[dict[str, Any]]) -> str | None:
    """Return canonical ``id`` when ``symbol_name`` matches a registry row."""
    symbol_key = fold_registry_token(symbol_name)
    for component in registry:
        candidates = registry_row_lookup_keys(component)
        if symbol_key in candidates:
            return str(component["id"])
        if any(symbol_key and symbol_key in c for c in candidates):
            return str(component["id"])
    return None


def stable_registry_row_payload(row: dict[str, Any]) -> str:
    """JSON envelope for one registry row fingerprint."""
    canon = {
        "component_schema": COMPONENT_SCHEMA_V11,
        "id": str(row.get("id", "")),
        "name": str(row.get("name", "")),
    }
    tier = row.get("tier")
    if tier is not None:
        canon["tier"] = str(tier)
    kind = row.get("kind")
    if kind is not None:
        canon["kind"] = str(kind)
    return json.dumps(canon, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def fingerprint_registry_row(row: dict[str, Any]) -> str:
    return hashlib.sha256(stable_registry_row_payload(row).encode("utf-8")).hexdigest()


def registry_snapshot_ledger(registry: list[dict[str, Any]]) -> dict[str, Any]:
    """Sorted snapshot: per-id fingerprints + aggregate sha256."""
    rows = [r for r in registry if r.get("id")]
    rows.sort(key=lambda r: str(r["id"]))
    by_id = {str(r["id"]): fingerprint_registry_row(r) for r in rows}
    payload = json.dumps(
        {"fingerprints_by_id": by_id, "schema": REGISTRY_SNAPSHOT_SCHEMA},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return {
        "registry_snapshot_schema": REGISTRY_SNAPSHOT_SCHEMA,
        "component_count": len(by_id),
        "fingerprints_by_id": by_id,
        "registry_snapshot_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
    }


_GAP_PROPOSAL_KEYS = (
    "dedup_key",
    "description",
    "fulfills_blueprints",
    "id",
    "kind",
    "made_of",
    "name",
    "product_categories",
    "sibling_source_count",
    "source_rank",
    "source_symbol",
    "tier",
)


def fingerprint_gap_proposal(record: dict[str, Any]) -> str:
    """Sha256 over stable gap-fill proposal fields (excludes prior fingerprint)."""
    slim = {k: record.get(k) for k in _GAP_PROPOSAL_KEYS}
    payload = json.dumps(slim, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
