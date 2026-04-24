"""Tier a1 — assimilated function 'optimize_swarm'

Assimilated from: aso.py:58-82
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
def optimize_swarm(
    repo: Annotated[Path | None, typer.Option(help="Repo root (default cwd)")] = None,
    topology: Annotated[str, typer.Option(help="parallel|sequential|hierarchical|adaptive")] = DEFAULT_SWARM_TOPOLOGY,
    memory_url: Annotated[str | None, typer.Option(help="Shared memory base URL (optional)")] = None,
) -> None:
    """SIE lane — swarm topology + optional memory endpoint."""
    if not is_valid_topology(topology):
        raise typer.BadParameter("invalid topology")
    root = _repo_root(repo)
    paths = aso_layout_paths(root)
    paths["swarm_config"].parent.mkdir(parents=True, exist_ok=True)
    prev: dict[str, object] | None = None
    if paths["swarm_config"].is_file():
        prev = json.loads(paths["swarm_config"].read_text(encoding="utf-8"))
    merged = merge_swarm_config_payload(
        prev,
        topology=topology,
        shared_memory_endpoint=memory_url,
        notes="Updated via ass-ade optimize swarm",
    )
    paths["swarm_config"].write_text(json.dumps(merged, indent=2), encoding="utf-8")
    plan = plan_swarm_intelligence(root)
    log_path = _write_log(root, "swarm", {"plan": plan, "config_written": str(paths["swarm_config"])})
    console.print(f"[green]Config[/green] {paths['swarm_config']}")
    console.print(f"[green]Log[/green] {log_path}")

