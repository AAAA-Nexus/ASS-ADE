"""Tier a1 — assimilated function 'scan'

Assimilated from: finish.py:19-36
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import os
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from ass_ade.engine.rebuild.finish import finish_project, scan_path


# --- assimilated symbol ---
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

