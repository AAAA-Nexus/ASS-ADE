import pytest

from ass_ade.local.planner import draft_plan, render_markdown


def test_draft_plan_respects_max_steps() -> None:
    plan = draft_plan("Integrate AAAA-Nexus MCP discovery", max_steps=3)

    assert len(plan) == 3
    assert plan[0].startswith("Define success criteria")


def test_draft_plan_rejects_empty_goal() -> None:
    with pytest.raises(ValueError):
        draft_plan("   ")


def test_render_markdown_contains_goal_and_steps() -> None:
    steps = draft_plan("Write onboarding docs", max_steps=2)
    rendered = render_markdown("Write onboarding docs", steps)

    assert "Goal: Write onboarding docs" in rendered
    assert "1. " in rendered
