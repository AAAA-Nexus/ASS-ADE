"""Tier a1 — assimilated function 'providers_set_chain'

Assimilated from: providers.py:320-333
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
def providers_set_chain(
    chain: Annotated[str, typer.Argument(help="Comma-separated provider names (e.g., 'groq,gemini,ollama').")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Override the provider fallback chain."""
    target, settings = _resolve_config(config)
    names = [n.strip() for n in chain.split(",") if n.strip()]
    invalid = [n for n in names if get_provider(n) is None]
    if invalid:
        console.print(f"[red]Unknown providers:[/red] {', '.join(invalid)}")
        raise typer.Exit(code=1)
    settings.provider_fallback_chain = names
    _save_config(target, settings)
    console.print(f"[green]✓[/green] Fallback chain: {' → '.join(names)}")

