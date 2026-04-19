# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_plan.py:7
# Component id: at.source.a1_at_functions.plan
from __future__ import annotations

__version__ = "0.1.0"

def plan(
    goal: str = typer.Argument(..., help="Goal to break into a public-safe draft plan."),
    max_steps: int = typer.Option(5, min=1, max=10, help="Maximum number of steps to emit."),
    markdown: bool = typer.Option(False, help="Render the plan as Markdown."),
) -> None:
    steps = draft_plan(goal, max_steps=max_steps)
    if markdown:
        console.print(render_markdown(goal, steps))
        return

    table = Table(title="Draft Plan")
    table.add_column("#", justify="right")
    table.add_column("Step")
    for index, step in enumerate(steps, start=1):
        table.add_row(str(index), step)
    console.print(table)
