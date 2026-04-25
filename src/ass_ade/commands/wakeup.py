"""Wakeup command: awareness-based greeting with no scheduler."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from ass_ade.a1_at_functions.speech import speak_greeting
from ass_ade.a2_mo_composites.ambient_awareness import AmbientAwareness

console = Console()


def wakeup_command(
    path: Annotated[
        Path,
        typer.Option(
            "--path",
            "-p",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Repo root or working directory to sense.",
        ),
    ] = Path("."),
    check: Annotated[
        bool,
        typer.Option("--check", help="Only report awareness state; do not open anything."),
    ] = False,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            help="Bypass awareness gating for a deliberate operator/agent action.",
        ),
    ] = False,
    json_out: Annotated[
        bool,
        typer.Option("--json", help="Print JSON instead of a short human report."),
    ] = False,
) -> None:
    """Sense whether it is time for Atomadic's unscheduled wakeup moment."""
    awareness = AmbientAwareness(repo_root=path)

    if check:
        report = awareness.report(force=force)
        if json_out:
            console.print_json(data=report)
            return
        console.print(f"[bold]Should greet:[/bold] {report['should_greet']}")
        console.print(f"[bold]Reason:[/bold] {report['reason']}")
        console.print(f"[dim]Template: {report['wake_template']}[/dim]")
        console.print("[dim]No browser opened. No scheduled task installed.[/dim]")
        return

    result = awareness.open_wake_page(force=force)
    if json_out:
        console.print_json(data=result)
        return
    if result["opened"]:
        console.print("[green]Atomadic opened the wake page.[/green]")
        console.print(f"[dim]{result.get('path', '')}[/dim]")
        speak_greeting()
    else:
        console.print("[yellow]Atomadic did not open the wake page.[/yellow]")
    console.print(str(result["reason"]))
    console.print("[dim]No cron, timer, or scheduled task was created.[/dim]")
