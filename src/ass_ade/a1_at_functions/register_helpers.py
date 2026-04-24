"""Tier a1 — assimilated function 'register'

Assimilated from: workflow.py:65-71
"""

from __future__ import annotations

# --- imports from original module ---
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx
import typer
from rich.console import Console

from ass_ade.config import default_config_path, load_config
from ass_ade.nexus.client import NexusClient


# --- assimilated symbol ---
def register(app: typer.Typer) -> None:
    """Register workflow commands on the provided app."""
    app.command("phase0-recon")(workflow_phase0_recon)
    app.command("trust-gate")(workflow_trust_gate)
    app.command("certify")(workflow_certify)
    app.command("safe-execute")(workflow_safe_execute)
    app.command("map-terrain")(workflow_map_terrain)

