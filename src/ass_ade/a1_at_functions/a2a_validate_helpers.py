"""Tier a1 — assimilated function 'a2a_validate'

Assimilated from: a2a.py:51-95
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path
from typing import Annotated, Any

import httpx
import typer
from rich.console import Console

from ass_ade.a2a import fetch_agent_card, local_agent_card, negotiate
from ass_ade.config import default_config_path, load_config
from ass_ade.nexus.client import NexusClient


# --- assimilated symbol ---
def a2a_validate(
    agent_card_path: Annotated[Path, typer.Argument(help="Path to the card.")],
) -> None:
    """Validate an A2A agent card format and structure."""
    from ass_ade.a2a import validate_agent_card

    if not agent_card_path.exists():
        console.print(f"[red]Error:[/red] File not found: {agent_card_path}")
        raise typer.Exit(code=1)

    try:
        data = json.loads(agent_card_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        console.print(f"[red]Error:[/red] Failed to parse JSON: {exc}")
        raise typer.Exit(code=1) from exc

    # Use library validation
    report = validate_agent_card(data)

    # Display validation results
    if report.valid:
        console.print("[green]✓ Valid A2A Agent Card[/green]")
    else:
        console.print("[red]✗ Invalid A2A Agent Card[/red]")

    # Show errors
    if report.errors:
        console.print("\n[red]Errors:[/red]")
        for issue in report.errors:
            console.print(f"  • {issue.field}: {issue.message}")

    # Show warnings
    if report.warnings:
        console.print("\n[yellow]Warnings:[/yellow]")
        for issue in report.warnings:
            console.print(f"  • {issue.field}: {issue.message}")

    # Show parsed card
    if report.card:
        console.print("\n[bold]Card Details:[/bold]")
        console.print(json.dumps(report.card.model_dump(), indent=2), markup=False)

    # Exit with error code if validation failed
    if not report.valid:
        raise typer.Exit(code=1)

