# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_render_markdown.py:7
# Component id: at.source.a1_at_functions.render_markdown
from __future__ import annotations

__version__ = "0.1.0"

def render_markdown(goal: str, steps: list[str]) -> str:
    lines = ["# Draft Plan", "", f"Goal: {goal}", ""]
    lines.extend(f"{index}. {step}" for index, step in enumerate(steps, start=1))
    return "\n".join(lines)
