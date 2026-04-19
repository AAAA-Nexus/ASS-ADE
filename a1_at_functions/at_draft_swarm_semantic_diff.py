# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_swarm_semantic_diff.py:7
# Component id: at.source.a1_at_functions.swarm_semantic_diff
from __future__ import annotations

__version__ = "0.1.0"

def swarm_semantic_diff(
    text_a: str = typer.Argument(..., help="First text."),
    text_b: str = typer.Argument(..., help="Second text."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Semantic diff between two texts. $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.agent_semantic_diff(base=text_a, current=text_b)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
