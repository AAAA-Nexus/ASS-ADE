# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_pipeline_status.py:7
# Component id: at.source.a1_at_functions.pipeline_status
from __future__ import annotations

__version__ = "0.1.0"

def pipeline_status(
    workflow_id: Annotated[str, typer.Argument(help="Workflow ID or filename.")],
) -> None:
    workflow_dir = Path.cwd() / ".ass-ade" / "workflows"
    if not workflow_dir.exists():
        console.print("[yellow]No workflows found in .ass-ade/workflows/[/yellow]")
        return

    target = workflow_dir / workflow_id
    if not target.exists():
        matches = list(workflow_dir.glob(f"{workflow_id}*"))
        if not matches:
            console.print(f"[red]Workflow not found:[/red] {workflow_id}")
            return
        target = matches[0]

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
        _print_json(data)
    except (json.JSONDecodeError, OSError) as exc:
        console.print(f"[red]Error reading workflow:[/red] {exc}")
