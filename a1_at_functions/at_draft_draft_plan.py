# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_draft_plan.py:7
# Component id: at.source.a1_at_functions.draft_plan
from __future__ import annotations

__version__ = "0.1.0"

def draft_plan(goal: str, max_steps: int = 5) -> list[str]:
    if not goal.strip():
        raise ValueError("Goal must not be empty.")

    _, steps = _detect_track(goal)
    intro = f"Define success criteria for: {goal.strip()}"
    plan = [intro, *steps]
    return plan[:max_steps]
