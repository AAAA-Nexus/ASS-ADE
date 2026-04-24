"""Tier a1 — assimilated function 'providers_env'

Assimilated from: providers.py:336-354
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
def providers_env(
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Print env-var hints + signup URLs for every provider."""
    table = Table(title="Provider env vars")
    table.add_column("Provider", style="bold")
    table.add_column("Env var")
    table.add_column("Set?")
    table.add_column("Signup")

    for name, profile in FREE_PROVIDERS.items():
        env_name = profile.api_key_env or "(no key)"
        set_status = "[green]✓[/green]" if (profile.api_key_env and os.getenv(profile.api_key_env)) else "[dim]—[/dim]"
        if profile.local:
            set_status = "[yellow]local[/yellow]"
        signup = profile.signup_url or ""
        table.add_row(profile.display_name, env_name, set_status, signup)
    console.print(table)
    console.print("\n[dim]Add any of these to your .env file at the project root.[/dim]")

