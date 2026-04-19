# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_planner.py:13
# Component id: at.source.ass_ade.test_draft_plan_rejects_empty_goal
__version__ = "0.1.0"

def test_draft_plan_rejects_empty_goal() -> None:
    with pytest.raises(ValueError):
        draft_plan("   ")
