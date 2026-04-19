# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_oracle_hallucination.py:7
# Component id: at.source.a1_at_functions.oracle_hallucination
from __future__ import annotations

__version__ = "0.1.0"

def oracle_hallucination(
    text: str = typer.Argument(..., help="Text to analyse for hallucination risk."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write JSON result to this path."),
) -> None:
    """Run the Hallucination Oracle — certified upper bound on confabulation. $0.040/request."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.hallucination_oracle(text=text)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    data = result.model_dump()
    _print_json(data)
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(data, indent=2), encoding="utf-8")
