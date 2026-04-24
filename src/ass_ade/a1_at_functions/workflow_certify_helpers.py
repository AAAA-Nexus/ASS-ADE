"""Tier a1 — assimilated function 'workflow_certify'

Assimilated from: workflow.py:155-189
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
def workflow_certify(
    text: str = typer.Argument(..., help="Text to certify."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: bool = typer.Option(False, "--json", help="Output raw JSON."),
) -> None:
    """Multi-step output certification: hallucination → ethics → compliance → certify → lineage."""
    from ass_ade.nexus.errors import NexusError
    from ass_ade.workflows import certify_output

    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = certify_output(client, text)
    except NexusError as exc:
        console.print(f"[red]Workflow error: {exc.detail}[/red]")
        raise typer.Exit(code=3) from exc
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    if json_out:
        _print_json(result.model_dump())
    else:
        color = "green" if result.passed else "red"
        console.print(f"[{color}]Passed: {result.passed}[/{color}]")
        console.print(f"  Certificate: {result.certificate_id or 'none'}")
        console.print(f"  Lineage: {result.lineage_id or 'none'}")
        console.print(f"  Hallucination: {result.hallucination_verdict}")
        console.print(f"  Ethics: {result.ethics_verdict}")
        console.print(f"  Compliance: {result.compliance_verdict}")

