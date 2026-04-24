"""Tier a1 — assimilated function 'workflow_map_terrain'

Assimilated from: workflow.py:228-329
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
def workflow_map_terrain(
    task_description: str = typer.Argument(
        ..., help="Task to validate before execution."
    ),
    agent: list[str] = typer.Option([], "--agent", help="Required agent capability."),
    hook: list[str] = typer.Option([], "--hook", help="Required hook capability."),
    skill: list[str] = typer.Option([], "--skill", help="Required skill capability."),
    tool: list[str] = typer.Option([], "--tool", help="Required tool capability."),
    harness: list[str] = typer.Option(
        [], "--harness", help="Required harness capability."
    ),
    prompt: list[str] = typer.Option(
        [], "--prompt", help="Required prompt capability."
    ),
    instruction: list[str] = typer.Option(
        [], "--instruction", help="Required instruction capability."
    ),
    requirements_file: Path | None = typer.Option(
        None, help="JSON file with grouped required_capabilities."
    ),
    auto_invent: bool = typer.Option(
        False,
        "--auto-invent",
        help="Generate repo-native assets plus certified rebuild packets for missing capabilities within budget.",
    ),
    max_budget: float = typer.Option(1.0, help="Maximum development budget in USDC."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """MAP = TERRAIN gate: halt and invent when required capabilities are missing."""
    from ass_ade.map_terrain import map_terrain

    _, settings = _resolve_config(config)
    required: dict[str, list[str]] = {
        "agents": list(agent),
        "hooks": list(hook),
        "skills": list(skill),
        "tools": list(tool),
        "harnesses": list(harness),
        "prompts": list(prompt),
        "instructions": list(instruction),
    }
    if requirements_file is not None:
        try:
            loaded = json.loads(requirements_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"[red]Failed to read requirements:[/red] {exc}")
            raise typer.Exit(code=4) from exc
        if isinstance(loaded, dict) and "required_capabilities" in loaded:
            loaded = loaded["required_capabilities"]
        if not isinstance(loaded, dict):
            console.print("[red]Requirements file must contain an object.[/red]")
            raise typer.Exit(code=4)
        for key, value in loaded.items():
            if value is None:
                continue
            if isinstance(value, str):
                required[key] = [value] if value.strip() else []
            elif isinstance(value, (list, tuple, set)):
                required[key] = [str(item) for item in value if str(item).strip()]

    hosted_tools: list[str] = []
    if settings.profile != "local" or allow_remote:
        try:
            with NexusClient(
                base_url=settings.nexus_base_url,
                timeout=settings.request_timeout_s,
                api_key=settings.nexus_api_key,
            ) as client:
                manifest = client.get_mcp_manifest()
            hosted_tools = [item.name or "" for item in manifest.tools]
        except httpx.HTTPError:
            hosted_tools = []

    result = map_terrain(
        task_description=task_description,
        required_capabilities=required,
        agent_id=settings.agent_id,
        max_development_budget_usdc=max_budget,
        auto_invent_if_missing=auto_invent,
        working_dir=Path("."),
        hosted_tools=hosted_tools,
    )

    if json_out:
        _print_json(result.model_dump(), redact=True)
        return

    color = "green" if result.verdict == "PROCEED" else "yellow"
    console.print(f"[{color}]MAP = TERRAIN: {result.verdict}[/{color}]")
    if result.missing_capabilities:
        console.print("[bold]Missing capabilities:[/bold]")
        for item in result.missing_capabilities:
            console.print(
                f"  - {item.type}: {item.name} via {item.recommended_creation_tool}"
            )
    console.print(f"Next: {result.next_action}")
    if result.development_plan and result.development_plan.created_assets:
        console.print("[bold]Created development-plan assets:[/bold]")
        for path in result.development_plan.created_assets:
            console.print(f"  - {path}")

