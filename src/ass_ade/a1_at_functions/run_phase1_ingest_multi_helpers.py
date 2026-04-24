"""Tier a1 — assimilated function 'run_phase1_ingest_multi'

Assimilated from: phase1_ingest.py:33-84
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from ass_ade.a0_qk_constants.policy_types import RootPolicy
from ass_ade.a1_at_functions.ingest import ingest_project


# --- assimilated symbol ---
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

    def _ingest_pair(pair: tuple[Path, str]) -> dict[str, Any]:
        r, rid = pair
        return ingest_project(r, root_id=rid, registry=registry, policy=plan.get(r))

    pairs = list(zip(roots, rids))
    raw_w = (os.environ.get("ASS_ADE_INGEST_MAX_WORKERS") or "").strip()
    if raw_w:
        try:
            max_workers = max(1, int(raw_w, 10))
        except ValueError:
            max_workers = min(8, len(pairs))
    else:
        max_workers = min(8, len(pairs))
    if len(pairs) <= 1 or max_workers <= 1:
        ingestions = [_ingest_pair(p) for p in pairs]
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            ingestions = list(pool.map(_ingest_pair, pairs))
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

