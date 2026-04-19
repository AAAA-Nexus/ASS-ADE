# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_normalize_branch_tracks.py:7
# Component id: at.source.a1_at_functions.normalize_branch_tracks
from __future__ import annotations

__version__ = "0.1.0"

def normalize_branch_tracks(branches: Iterable[str]) -> list[str]:
    normalized: list[str] = []
    for branch in branches:
        item = branch.strip()
        if not item:
            continue
        item = re.sub(r"[^A-Za-z0-9/_-]+", "-", item).strip("-/")
        if not item:
            continue
        if not item.startswith("evolve/"):
            item = f"evolve/{item}"
        normalized.append(item)
    return normalized or ["evolve/tests-first", "evolve/docs-first", "evolve/safety-first"]
