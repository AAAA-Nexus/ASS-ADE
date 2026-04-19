# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_planner.py:18
# Component id: at.source.ass_ade.test_render_markdown_contains_goal_and_steps
__version__ = "0.1.0"

def test_render_markdown_contains_goal_and_steps() -> None:
    steps = draft_plan("Write onboarding docs", max_steps=2)
    rendered = render_markdown("Write onboarding docs", steps)

    assert "Goal: Write onboarding docs" in rendered
    assert "1. " in rendered
