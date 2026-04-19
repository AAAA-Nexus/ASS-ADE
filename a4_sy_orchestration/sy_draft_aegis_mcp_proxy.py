# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2406
# Component id: sy.source.ass_ade.aegis_mcp_proxy
from __future__ import annotations

__version__ = "0.1.0"

def aegis_mcp_proxy(
    tool_name: str = typer.Argument(..., help="MCP tool name to proxy."),
    payload_file: Path | None = typer.Option(None, help="JSON payload file."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Route MCP tool calls through AEGIS safety layer. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    payload: dict = {}
    if payload_file:
        try:
            payload = json.loads(payload_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"Failed to read payload: {exc}")
            raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.aegis_mcp_proxy(tool_name=tool_name, payload=payload)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
