# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1350
# Component id: at.source.ass_ade.pipeline_status
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
