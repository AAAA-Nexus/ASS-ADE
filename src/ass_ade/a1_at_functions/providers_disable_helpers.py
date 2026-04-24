"""Tier a1 — assimilated function 'providers_disable'

Assimilated from: providers.py:248-253
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
def providers_disable(
    name: Annotated[str, typer.Argument(help="Provider name to disable.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Disable a provider (exclude from the fallback chain)."""
    _set_enabled(name, False, config)

