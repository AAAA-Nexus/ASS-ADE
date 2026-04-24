"""Tier a1 — assimilated function 'workflow_safe_execute'

Assimilated from: workflow.py:192-225
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
def workflow_safe_execute(
    tool_name: str = typer.Argument(..., help="MCP tool name to execute."),
    tool_input: str = typer.Argument("", help="Input to the tool."),
    agent_id: str | None = typer.Option(None, help="Agent ID for AEGIS proxy."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """AEGIS-wrapped MCP tool execution: shield → scan → proxy → certify."""
    from ass_ade.nexus.errors import NexusError
    from ass_ade.workflows import safe_execute

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = safe_execute(client, tool_name, tool_input, agent_id=agent_id)
    except NexusError as exc:
        console.print(f"[red]Workflow error: {exc.detail}[/red]")
        raise typer.Exit(code=3) from exc
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    if json_out:
        _print_json(result.model_dump())
    else:
        console.print(f"  Tool: {result.tool_name}")
        console.print(f"  Shield: {'✓' if result.shield_passed else '✗'}")
        console.print(f"  Prompt Scan: {'✓' if result.prompt_scan_passed else '✗'}")
        console.print(f"  Certificate: {result.certificate_id or 'none'}")

