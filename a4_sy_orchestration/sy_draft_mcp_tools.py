# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_mcp_tools.py:7
# Component id: sy.source.a4_sy_orchestration.mcp_tools
from __future__ import annotations

__version__ = "0.1.0"

def mcp_tools(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """List tools published in the MCP manifest."""
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

    table = Table(title="MCP Tools")
    table.add_column("#", justify="right")
    table.add_column("Name")
    table.add_column("Endpoint")
    table.add_column("Method")
    table.add_column("Paid")
    for idx, tool in enumerate(manifest.tools, start=1):
        table.add_row(
            str(idx), tool.name or "n/a", tool.endpoint or "n/a", tool.method
            or "POST", str(bool(tool.paid)),
        )
    console.print(table)
