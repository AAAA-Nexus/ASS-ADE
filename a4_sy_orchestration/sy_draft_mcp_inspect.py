# Extracted from C:/!ass-ade/src/ass_ade/cli.py:902
# Component id: sy.source.ass_ade.mcp_inspect
from __future__ import annotations

__version__ = "0.1.0"

def mcp_inspect(
    identifier: str = typer.Argument(..., help="Tool name or index (1-based)."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Show full MCP tool metadata for a named tool or numeric index."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url, timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key
        ) as client:
            manifest = client.get_mcp_manifest()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return

    tool = resolve_tool(manifest, identifier)
    if tool is None:
        console.print(f"Tool not found: {identifier}")
        raise typer.Exit(code=2)

    _print_json(tool)
