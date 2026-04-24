"""CLI sub-command: ``ass-ade finish`` — complete partial codebases."""

from __future__ import annotations

import os
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ass_ade.engine.rebuild.finish import finish_project, scan_path

finish_app = typer.Typer(help="Complete 20–80% codebases: fill stub bodies via refinement loop.")
_console = Console()


@finish_app.command("scan")
def scan(
    path: Path = typer.Argument(Path("."), help="Project root to scan."),
    limit: int = typer.Option(50, help="Maximum items to list."),
) -> None:
    """List incomplete functions/methods detected under ``path``."""
    items = scan_path(path.resolve())
    if not items:
        _console.print("[green]no incomplete functions detected[/green]")
        return
    table = Table(title=f"Incomplete functions under {path}")
    table.add_column("file", style="cyan")
    table.add_column("qualname")
    table.add_column("line", justify="right")
    table.add_column("reason", style="yellow")
    for fn in items[:limit]:
        table.add_row(str(fn.path), fn.qualname, str(fn.lineno), fn.reason)
    _console.print(table)
    _console.print(f"\ntotal: {len(items)}")


@finish_app.command("run")
def run(
    path: Path = typer.Argument(Path("."), help="Project root to complete."),
    apply: bool = typer.Option(
        False, "--apply", help="Write completions back to source files (destructive)."
    ),
    out: Path = typer.Option(
        None, "--out", help="Override patch output directory."
    ),
    max_refine: int = typer.Option(3, help="Refinement attempts per function."),
    max_functions: int = typer.Option(100, help="Maximum functions to process."),
    nexus_url: str = typer.Option(None, help="Override AAAA-Nexus base URL."),
) -> None:
    """Run the completion pipeline. Writes patches under ``.ass-ade/patches/``."""
    root = path.resolve()
    if not root.exists():
        _console.print(f"[red]path not found:[/red] {root}")
        raise typer.Exit(code=1)
    _console.print(f"[bold]ass-ade finish run[/bold] :: {root}")
    _console.print(f"  apply:  {apply}")
    _console.print(f"  refine: {max_refine}")

    resolved_url = nexus_url or os.environ.get("AAAA_NEXUS_BASE_URL")
    kwargs: dict[str, object] = {}
    if resolved_url:
        kwargs["base_url"] = resolved_url
    receipt = finish_project(
        root,
        api_key=os.environ.get("AAAA_NEXUS_API_KEY"),
        agent_id=os.environ.get("AAAA_NEXUS_AGENT_ID"),
        out_dir=out.resolve() if out else None,
        apply_in_place=apply,
        max_refinement_attempts=max_refine,
        max_functions=max_functions,
        **kwargs,  # type: ignore[arg-type]
    )

    _console.print("[green]finish complete[/green]")
    _console.print(f"  scanned:   {receipt['scanned_functions']}")
    _console.print(f"  completed: {receipt['completed_count']}")
    _console.print(f"  rejected:  {receipt['rejected_count']}")
    _console.print(f"  patches:   {receipt['out_dir']}")
    if receipt["rejected_count"]:
        raise typer.Exit(code=2)
