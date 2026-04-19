# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_swarm_token_budget.py:7
# Component id: qk.source.a0_qk_constants.swarm_token_budget
from __future__ import annotations

__version__ = "0.1.0"

def swarm_token_budget(
    text: str = typer.Argument(..., help="Text to estimate token budget for."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Estimate token budget across models. $0.008/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.agent_token_budget(task=text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
