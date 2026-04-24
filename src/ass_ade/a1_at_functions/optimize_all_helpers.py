"""Tier a1 — assimilated function 'optimize_all'

Assimilated from: aso.py:108-115
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.console import Console
from rich.syntax import Syntax

from ass_ade.aso.constants import DEFAULT_SWARM_TOPOLOGY
from ass_ade.aso.plan import (


# --- assimilated symbol ---
def optimize_all(
    repo: Annotated[Path | None, typer.Option(help="Repo root (default cwd)")] = None,
) -> None:
    """Emit a combined ASO plan JSON (all four engines)."""
    root = _repo_root(repo)
    bundle = plan_full_aso(root)
    path = _write_log(root, "full", bundle)
    console.print(f"[green]Wrote[/green] {path}")

