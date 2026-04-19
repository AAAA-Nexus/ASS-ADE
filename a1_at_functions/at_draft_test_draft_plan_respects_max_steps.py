# Extracted from C:/!ass-ade/tests/test_planner.py:6
# Component id: at.source.ass_ade.test_draft_plan_respects_max_steps
from __future__ import annotations

__version__ = "0.1.0"

def test_draft_plan_respects_max_steps() -> None:
    plan = draft_plan("Integrate AAAA-Nexus MCP discovery", max_steps=3)

    assert len(plan) == 3
    assert plan[0].startswith("Define success criteria")
