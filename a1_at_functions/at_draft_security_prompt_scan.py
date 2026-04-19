# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_security_prompt_scan.py:7
# Component id: at.source.a1_at_functions.security_prompt_scan
from __future__ import annotations

__version__ = "0.1.0"

def security_prompt_scan(
    prompt: str = typer.Argument(..., help="Prompt text to scan for injection."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Prompt injection scanner. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.prompt_inject_scan(prompt=prompt)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    verdict = "THREAT DETECTED" if result.threat_detected else "CLEAN"
    console.print(f"{verdict}  level={result.threat_level}  confidence={result.confidence}")
