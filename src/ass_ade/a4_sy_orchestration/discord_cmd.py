"""Tier a4 — CLI commands for the Atomadic Discord bot."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Annotated

import typer

discord_app = typer.Typer(
    name="discord",
    help="Atomadic Discord bot — start the bot or manage its configuration.",
    no_args_is_help=True,
)

_SCRIPTS_DIR = Path(__file__).resolve().parents[3] / "scripts"


@discord_app.command("start")
def start(
    script: Annotated[
        Path,
        typer.Option(
            "--script",
            help="Path to the Discord bot script.",
            show_default=True,
        ),
    ] = _SCRIPTS_DIR / "atomadic_discord_bot.py",
) -> None:
    """Start the Atomadic Discord bot.

    Reads DISCORD_BOT_TOKEN and AAAA_NEXUS_API_KEY from .env.
    Keep this process running — Ctrl+C to stop.
    """
    if not script.exists():
        typer.secho(f"Bot script not found: {script}", fg=typer.colors.RED, err=True)
        typer.secho(
            "Expected location: scripts/atomadic_discord_bot.py in the project root.",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(1)

    typer.secho(f"Starting Atomadic Discord bot from {script}", fg=typer.colors.CYAN)
    typer.secho("Press Ctrl+C to stop.\n", fg=typer.colors.YELLOW)

    result = subprocess.run([sys.executable, str(script)])
    raise typer.Exit(result.returncode)
