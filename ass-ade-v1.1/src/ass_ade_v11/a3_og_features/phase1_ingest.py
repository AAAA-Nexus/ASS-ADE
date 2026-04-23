"""Phase 1 — ingest sources into candidate components."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade_v11.a0_qk_constants.policy_types import RootPolicy
from ass_ade_v11.a1_at_functions.ingest import ingest_project


def run_phase1_ingest(
    source_root: Path,
    *,
    root_id: str | None = None,
    registry: list[dict[str, Any]] | None = None,
    policy_by_root: dict[Path, RootPolicy] | None = None,
) -> dict[str, Any]:
    source_root = source_root.resolve()
    rid = root_id if root_id is not None else source_root.name
    policy = (policy_by_root or {}).get(source_root)
    ingestion = ingest_project(source_root, root_id=rid, registry=registry, policy=policy)
    return {
        "phase": 1,
        "ingestion": ingestion,
        "ingestions": [ingestion],
        "summary": ingestion["summary"],
    }


def run_phase1_ingest_multi(
    source_roots: list[Path],
    *,
    root_ids: list[str] | None = None,
    registry: list[dict[str, Any]] | None = None,
    policy_by_root: dict[Path, RootPolicy] | None = None,
) -> dict[str, Any]:
    """Ingest each root; gap-fill merges ``ingestions`` into one assimilated plan."""
    roots = [Path(p).resolve() for p in source_roots]
    if root_ids is None:
        rids = [p.name for p in roots]
    else:
        rids = list(root_ids)
        if len(rids) != len(roots):
            raise ValueError("root_ids must be the same length as source_roots")

    plan = policy_by_root or {}
    ingestions = [
        ingest_project(r, root_id=rid, registry=registry, policy=plan.get(r))
        for r, rid in zip(roots, rids)
    ]
    reg = registry or []
    merged = {
        "sources": len(roots),
        "files_scanned": sum(x["summary"]["files_scanned"] for x in ingestions),
        "symbols": sum(x["summary"]["symbols"] for x in ingestions),
        "candidate_components": sum(x["summary"]["candidate_components"] for x in ingestions),
        "mapped": sum(x["summary"]["mapped"] for x in ingestions),
        "gaps": sum(x["summary"]["gaps"] for x in ingestions),
        "by_tier": _merge_by_tier(ingestions),
    }
    return {
        "phase": 1,
        "ingestion": ingestions[0],
        "ingestions": ingestions,
        "summary": merged,
    }


def _merge_by_tier(ingestions: list[dict[str, Any]]) -> dict[str, int]:
    out: dict[str, int] = {}
    for ing in ingestions:
        for tier, n in (ing.get("summary") or {}).get("by_tier", {}).items():
            out[str(tier)] = out.get(str(tier), 0) + int(n)
    return out
