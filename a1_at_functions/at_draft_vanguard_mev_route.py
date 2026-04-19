# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_vanguard_mev_route.py:7
# Component id: at.source.a1_at_functions.vanguard_mev_route
from __future__ import annotations

__version__ = "0.1.0"

def vanguard_mev_route(
    agent_id: str = typer.Argument(..., help="Agent ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    intent_file: Path | None = typer.Option(None, help="JSON file with route intent."),
) -> None:
    """MEV route intent governance. $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    intent: dict = {}
    if intent_file:
        try:
            intent = json.loads(intent_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            console.print(f"Failed to read intent file: {exc}")
            raise typer.Exit(code=4) from exc
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.vanguard_mev_route(agent_id=agent_id, intent=intent)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
