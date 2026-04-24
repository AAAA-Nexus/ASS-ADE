"""Tier a1 — assimilated function 'providers_enable'

Assimilated from: providers.py:240-245
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
def providers_enable(
    name: Annotated[str, typer.Argument(help="Provider name to enable.")],
    config: Path | None = CONFIG_OPTION,
) -> None:
    """Enable a provider (include it in the fallback chain)."""
    _set_enabled(name, True, config)

