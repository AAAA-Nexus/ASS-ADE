# Extracted from C:/!ass-ade/src/ass_ade/cli.py:2733
# Component id: at.source.ass_ade.bitnet_stream
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_stream(
    prompt: str = typer.Argument(..., help="Prompt to stream."),
    model: str = typer.Option("bitnet-b1.58-2B-4T", help="BitNet model ID."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Streaming 1.58-bit BitNet CoT inference (BIT-101). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            for chunk in client.bitnet_stream(prompt=prompt, model=model):
                console.print(chunk, end="")
    except httpx.HTTPError as exc:
        _nexus_err(exc)
