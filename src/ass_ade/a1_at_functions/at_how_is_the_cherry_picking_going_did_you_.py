"""Tier a1 — pure helper: report cherry-picking session status."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def how_is_the_cherry_picking_going_did_you_(
    project_root: str | Path | None = None,
) -> dict[str, Any]:
    """Return a summary of the most recent cherry-pick session.

    Reads .ass-ade/cherry_pick.json relative to *project_root* (defaults to
    cwd). Returns a plain dict — callers decide how to format it.
    """
    root = Path(project_root) if project_root else Path.cwd()
    session_path = root / ".ass-ade" / "cherry_pick.json"

    if not session_path.exists():
        return {
            "found": False,
            "selected_count": 0,
            "assimilate": 0,
            "rebuild": 0,
            "skip": 0,
            "source_label": "",
            "features": [],
        }

    try:
        data: dict[str, Any] = json.loads(session_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"found": False, "error": "could not parse cherry_pick.json"}

    items: list[dict[str, Any]] = data.get("items", [])
    assimilate = sum(1 for i in items if i.get("action") == "assimilate")
    rebuild = sum(1 for i in items if i.get("action") == "rebuild")
    skip = len(items) - assimilate - rebuild
    features = [i.get("qualname", "") for i in items if i.get("action") == "assimilate"]

    return {
        "found": True,
        "selected_count": data.get("selected_count", len(items)),
        "assimilate": assimilate,
        "rebuild": rebuild,
        "skip": skip,
        "source_label": data.get("source_label", ""),
        "features": features,
    }
