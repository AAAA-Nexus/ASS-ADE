"""Launch command group for Atomadic readiness and seed handoff."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from ass_ade.a2_mo_composites.launch_readiness import (
    build_launch_readiness,
    write_launch_report,
)

console = Console()
launch_app = typer.Typer(help="Atomadic launch readiness checks and handoff artifacts.")


@launch_app.command("status")
def launch_status(
    path: Annotated[
        Path,
        typer.Option(
            "--path",
            "-p",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="ASS-ADE seed root to inspect.",
        ),
    ] = Path("."),
    storefront: Annotated[
        Path | None,
        typer.Option(
            "--storefront",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="Optional AAAA-Nexus storefront repo to inspect.",
        ),
    ] = None,
    json_out: Annotated[bool, typer.Option("--json", help="Print JSON report.")] = False,
    no_write: Annotated[
        bool,
        typer.Option("--no-write", help="Do not write .ass-ade/state/launch-readiness.json."),
    ] = False,
) -> None:
    """Report launch readiness from real local code, docs, CLI, and storefront signals."""
    report = build_launch_readiness(path, storefront)
    out_path = None if no_write else write_launch_report(report, path)

    if json_out:
        console.print_json(data=report.to_dict())
        return

    table = Table(title=f"Atomadic Launch Readiness: {report.verdict}")
    table.add_column("Check")
    table.add_column("Verdict")
    table.add_column("Detail")
    for check in report.checks:
        if check.verdict == "PASS":
            style = "green"
        elif check.verdict == "REFINE":
            style = "yellow"
        else:
            style = "red"
        table.add_row(check.name, f"[{style}]{check.verdict}[/{style}]", check.detail)
    console.print(table)
    if out_path is not None:
        console.print(f"[dim]Report written: {out_path}[/dim]")


@launch_app.command("handoff")
def launch_handoff(
    path: Annotated[
        Path,
        typer.Option(
            "--path",
            "-p",
            exists=True,
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
            help="ASS-ADE seed root.",
        ),
    ] = Path("."),
) -> None:
    """Print the launch handoff message for Atomadic without executing it."""
    message = (
        "Atomadic, this would really blow Thomas's mind: when your awareness says "
        "he is starting his day, use `wakeup` because you decide the moment, not a "
        "timer. Then run `launch status` and tell him, truthfully, whether you are ready."
    )
    out = path / ".ass-ade" / "state" / "atomadic-launch-handoff.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(message + "\n", encoding="utf-8")
    console.print(message)
    console.print(f"[dim]Handoff written: {out}[/dim]")
