# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/cli.py:1373
# Component id: at.source.ass_ade.pipeline_history
__version__ = "0.1.0"

def pipeline_history(
    limit: Annotated[int, typer.Option(help="Limit number of items.")] = 10,
) -> None:
    import time
    workflow_dir = Path.cwd() / ".ass-ade" / "workflows"
    if not workflow_dir.exists():
        console.print("[yellow]No history found.[/yellow]")
        return

    files = sorted(workflow_dir.glob("*.json"), key=lambda x: x.stat().st_mtime, reverse=True)

    table = Table(title="Pipeline History")
    table.add_column("Date")
    table.add_column("Workflow")
    table.add_column("Result")
    table.add_column("Duration")

    for f in files[:limit]:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(f.stat().st_mtime))
            res = "[green]PASS[/green]" if data.get("passed") else "[red]FAIL[/red]"
            dur = f"{data.get('duration_ms', 0):.0f}ms"
            table.add_row(dt, data.get("name", f.name), res, dur)
        except (json.JSONDecodeError, OSError):
            continue

    console.print(table)
