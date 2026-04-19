# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/local/planner.py:49
# Component id: at.source.ass_ade.render_markdown
__version__ = "0.1.0"

def render_markdown(goal: str, steps: list[str]) -> str:
    lines = ["# Draft Plan", "", f"Goal: {goal}", ""]
    lines.extend(f"{index}. {step}" for index, step in enumerate(steps, start=1))
    return "\n".join(lines)
