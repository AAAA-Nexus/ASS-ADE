# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_render_markdown_contains_goal_and_steps.py:7
# Component id: at.source.a1_at_functions.test_render_markdown_contains_goal_and_steps
from __future__ import annotations

__version__ = "0.1.0"

def test_render_markdown_contains_goal_and_steps() -> None:
    steps = draft_plan("Write onboarding docs", max_steps=2)
    rendered = render_markdown("Write onboarding docs", steps)

    assert "Goal: Write onboarding docs" in rendered
    assert "1. " in rendered
