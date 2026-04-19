# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_bitnet_chat.py:7
# Component id: at.source.a1_at_functions.bitnet_chat
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_chat(
    prompt: str = typer.Argument(..., help="Prompt for 1.58-bit inference."),
    model: str = typer.Option("bitnet-b1.58-2B-4T", help="BitNet model ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """1.58-bit BitNet chat completion (BIT-100). $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.bitnet_inference(prompt=prompt, model=model)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(result.result or "(no response)")
