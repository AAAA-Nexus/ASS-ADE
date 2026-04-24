"""Tier a1 — assimilated function 'experiments_from_track'

Assimilated from: rebuild/epiphany_cycle.py:98-115
"""

from __future__ import annotations


# --- assimilated symbol ---
def experiments_from_track(track: str, plan_steps: list[str]) -> list[dict[str, object]]:
    """Single default experiment slot; agents replace with repo-specific commands."""
    hint = "pytest -q path/to/tests"
    if track == "integration":
        hint = "python -m pytest tests/ -q --tb=no  # or MCP smoke against manifest"
    elif track == "documentation":
        hint = "docs link check or markdown linter configured for the repo"
    elif track == "validation":
        hint = "pytest -q on the highest-risk module named in recon"
    mid = plan_steps[1] if len(plan_steps) > 1 else (plan_steps[0] if plan_steps else "")
    return [
        {
            "id": "x1",
            "command_or_hint": hint,
            "success_criteria": "Exit 0 and no new failures vs baseline; record diff scope.",
            "grounding_from_plan": mid[:240],
        }
    ]

