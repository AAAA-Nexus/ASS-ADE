# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3573
# Component id: qk.source.ass_ade.inference_token_count
from __future__ import annotations

__version__ = "0.1.0"

def inference_token_count(
    task: Annotated[str, typer.Argument(help="Task description to estimate tokens for.")],
    models: Annotated[list[str] | None, typer.Option(help="Models to estimate for.")] = None,
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Cost estimate across 7 models. $0.020/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            result = client.agent_token_budget(task=task, models=models)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
    _print_json(result)
