"""Tier a2 — composite: format and return cherry-pick session status report."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from ass_ade.a1_at_functions.at_how_is_the_cherry_picking_going_did_you_ import (
    how_is_the_cherry_picking_going_did_you_,
)


def run_how_is_the_cherry_picking_going_did_you__pipeline(
    project_root: str | Path | None = None,
) -> dict[str, Any]:
    """Run the cherry-pick status pipeline and return a formatted report dict.

    Returns:
        status (str)        – 'active' | 'empty' | 'no_session'
        summary (str)       – one-line human-readable summary
        detail (dict)       – raw counts from the session file
    """
    detail = how_is_the_cherry_picking_going_did_you_(project_root)

    if not detail.get("found"):
        return {
            "status": "no_session",
            "summary": "No cherry-pick session found — run `atomadic cherry scout` to start one.",
            "detail": detail,
        }

    total = detail["selected_count"]
    assimilate = detail["assimilate"]
    rebuild = detail["rebuild"]
    features = detail["features"]

    if total == 0:
        status = "empty"
        summary = "Session file exists but contains no items."
    else:
        status = "active"
        parts = []
        if assimilate:
            parts.append(f"{assimilate} ready to assimilate")
        if rebuild:
            parts.append(f"{rebuild} need rebuild")
        feature_list = ", ".join(features[:5])
        suffix = f" — {feature_list}" if feature_list else ""
        summary = f"Cherry-pick session: {total} items ({'; '.join(parts)}){suffix}"

    return {"status": status, "summary": summary, "detail": detail}
