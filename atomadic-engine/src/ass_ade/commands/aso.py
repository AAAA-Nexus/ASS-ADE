"""a4 Typer entry — ``ass-ade optimize`` (Atomadic Swarm Optimizer orchestrator)."""

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
    plan_codebase_cortex,
    plan_context_optimization,
    plan_full_aso,
    plan_swarm_intelligence,
    plan_telemetry_evolution,
)
from ass_ade.aso.pure import aso_layout_paths, is_valid_topology, merge_swarm_config_payload

aso_app = typer.Typer(
    name="optimize",
    help="Atomadic Swarm Optimizer (ASO) — context, swarm, codebase, telemetry lanes.",
)
console = Console()


def _repo_root(explicit: Path | None) -> Path:
    return (explicit or Path.cwd()).resolve()


def _write_log(repo: Path, lane: str, payload: dict[str, Any]) -> Path:
    paths = aso_layout_paths(repo)
    log_root = paths["logs"]
    log_root.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = log_root / f"{lane}-{ts}.json"
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return out


@aso_app.command("context")
def optimize_context(
    repo: Annotated[Path | None, typer.Option(help="Repo root (default cwd)")] = None,
) -> None:
    """COE lane — MCP / schema compression plan (measurement-first)."""
    root = _repo_root(repo)
    plan = plan_context_optimization(root)
    path = _write_log(root, "context", plan)
    console.print(f"[green]Wrote[/green] {path}")
    console.print(Syntax(json.dumps(plan, indent=2), "json", theme="monokai", line_numbers=False))


@aso_app.command("swarm")
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


@aso_app.command("codebase")
def optimize_codebase(
    repo: Annotated[Path | None, typer.Option(help="Repo root (default cwd)")] = None,
) -> None:
    """CCE lane — graph + index hygiene plan."""
    root = _repo_root(repo)
    plan = plan_codebase_cortex(root)
    path = _write_log(root, "codebase", plan)
    console.print(f"[green]Wrote[/green] {path}")


@aso_app.command("telemetry")
def optimize_telemetry(
    repo: Annotated[Path | None, typer.Option(help="Repo root (default cwd)")] = None,
) -> None:
    """TEE lane — telemetry + evolution hooks plan."""
    root = _repo_root(repo)
    plan = plan_telemetry_evolution(root)
    path = _write_log(root, "telemetry", plan)
    console.print(f"[green]Wrote[/green] {path}")


@aso_app.command("all")
def optimize_all(
    repo: Annotated[Path | None, typer.Option(help="Repo root (default cwd)")] = None,
) -> None:
    """Emit a combined ASO plan JSON (all four engines)."""
    root = _repo_root(repo)
    bundle = plan_full_aso(root)
    path = _write_log(root, "full", bundle)
    console.print(f"[green]Wrote[/green] {path}")
