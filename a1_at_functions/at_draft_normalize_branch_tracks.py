# Extracted from C:/!ass-ade/src/ass_ade/protocol/evolution.py:637
# Component id: at.source.ass_ade.normalize_branch_tracks
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
