# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a4_sy_orchestration/sy_draft_mcp_estimate_cost.py:7
# Component id: sy.source.a4_sy_orchestration.mcp_estimate_cost
from __future__ import annotations

__version__ = "0.1.0"

def mcp_estimate_cost(
    identifier: str = typer.Argument(..., help="Tool name or index (1-based)."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Show cost and rate-limit metadata for a tool declared in the MCP manifest."""
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

    cost = estimate_cost(tool)
    if cost is None:
        console.print(f"Tool '{tool.name}' is free with no cost metadata.")
        return

    table = Table(title=f"Cost Estimate – {tool.name}")
    table.add_column("Field")
    table.add_column("Value")
    table.add_row("Currency", cost.currency)
    table.add_row("Unit Cost", str(cost.unit_cost) if cost.unit_cost is not None else "n/a")
    table.add_row("Rate Limit (req/min)", str(cost.rate_limit_rpm) if cost.rate_limit_rpm is not None else "n/a")
    table.add_row("Rate Limit (tokens/min)", str(cost.rate_limit_tpm) if cost.rate_limit_tpm is not None else "n/a")
    table.add_row("Notes", cost.notes or "—")
    console.print(table)
