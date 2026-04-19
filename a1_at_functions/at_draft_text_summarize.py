# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_text_summarize.py:7
# Component id: at.source.a1_at_functions.text_summarize
from __future__ import annotations

__version__ = "0.1.0"

def text_summarize(
    text: str = typer.Argument(..., help="Text to summarize."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Extractive text summarization — 1-3 sentences. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.text_summarize(text=text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(result.summary or "(no summary returned)")
