# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_workflow_safe_execute.py:7
# Component id: og.source.a3_og_features.workflow_safe_execute
from __future__ import annotations

__version__ = "0.1.0"

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
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
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
