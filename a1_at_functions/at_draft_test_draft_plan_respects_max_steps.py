# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_draft_plan_respects_max_steps.py:7
# Component id: at.source.a1_at_functions.test_draft_plan_respects_max_steps
from __future__ import annotations

__version__ = "0.1.0"

def test_draft_plan_respects_max_steps() -> None:
    plan = draft_plan("Integrate AAAA-Nexus MCP discovery", max_steps=3)

    assert len(plan) == 3
    assert plan[0].startswith("Define success criteria")
