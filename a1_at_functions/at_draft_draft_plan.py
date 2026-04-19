# Extracted from C:/!ass-ade/src/ass_ade/local/planner.py:39
# Component id: at.source.ass_ade.draft_plan
from __future__ import annotations

__version__ = "0.1.0"

def draft_plan(goal: str, max_steps: int = 5) -> list[str]:
    if not goal.strip():
        raise ValueError("Goal must not be empty.")

    _, steps = _detect_track(goal)
    intro = f"Define success criteria for: {goal.strip()}"
    plan = [intro, *steps]
    return plan[:max_steps]
