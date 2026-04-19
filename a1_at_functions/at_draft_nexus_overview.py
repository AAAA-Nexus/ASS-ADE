# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1100
# Component id: at.source.ass_ade.nexus_overview
from __future__ import annotations

__version__ = "0.1.0"

def nexus_overview(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            health = client.get_health()
            openapi = client.get_openapi()
            agent_card = client.get_agent_card()
            mcp_manifest = client.get_mcp_manifest()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return

    table = Table(title="AAAA-Nexus Overview")
    table.add_column("Signal")
    table.add_column("Value")
    table.add_row("Base URL", settings.nexus_base_url)
    table.add_row("Health Status", health.status)
    table.add_row("API Version", str(openapi.info.version or "unknown"))
    table.add_row("Agent Card Name", agent_card.name)
    table.add_row("Agent Skills", str(len(agent_card.skills)))
    table.add_row("MCP Tools", str(len(mcp_manifest.tools)))
    table.add_row(
        "Trial Policy",
        str(
            (agent_card.trialPolicy.note if agent_card.trialPolicy else None)
            or (agent_card.authentication.trialAccess if agent_card.authentication else None)
            or "n/a"
        ),
    )
    console.print(table)
