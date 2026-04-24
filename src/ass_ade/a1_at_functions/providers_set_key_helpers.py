"""Tier a1 — assimilated function 'providers_set_key'

Assimilated from: providers.py:296-317
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Annotated, Any

import httpx
import typer
from rich.console import Console
from rich.table import Table

from ass_ade.agent.providers import (


# --- assimilated symbol ---
def providers_set_key(
    provider: Annotated[str, typer.Argument(help="Provider name to set the API key for.")],
    api_key: Annotated[str, typer.Argument(help="API key value. NOT written to disk; session only.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Set a provider API key for this shell session (not persisted).

    For persistent keys, set the provider's env var in your .env file.
    Running `ass-ade providers env` prints the env vars per provider.
    """
    profile = get_provider(provider)
    if profile is None:
        console.print(f"[red]Unknown provider:[/red] {provider}")
        raise typer.Exit(code=1)
    if not profile.api_key_env:
        console.print(f"[yellow]{provider} doesn't use an API key.[/yellow]")
        raise typer.Exit(code=0)
    os.environ[profile.api_key_env] = api_key
    console.print(
        f"[green]✓[/green] {profile.api_key_env} set for this session.\n"
        f"[dim]To persist, add [bold]{profile.api_key_env}=...[/bold] to your .env file.[/dim]"
    )

