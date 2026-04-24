"""Tier a1 — assimilated function 'run_phase1_ingest'

Assimilated from: phase1_ingest.py:14-30
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

