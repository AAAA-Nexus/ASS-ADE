# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1979
# Component id: at.source.ass_ade.discovery_search
from __future__ import annotations

__version__ = "0.1.0"

def discovery_search(
    query: str = typer.Argument(..., help="Natural language search query."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Search for agents by capability. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.discovery_search(capability=query)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title=f"Discovery: {query}")
    table.add_column("Agent ID")
    table.add_column("Name")
    table.add_column("Score")
    for agent in result.agents:
        table.add_row(agent.agent_id or "", agent.name or "", str(agent.match_score or ""))
    console.print(table)
