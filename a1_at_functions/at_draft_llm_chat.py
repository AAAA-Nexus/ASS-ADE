# Extracted from C:/!ass-ade/src/ass_ade/cli.py:1688
# Component id: at.source.ass_ade.llm_chat
from __future__ import annotations

__version__ = "0.1.0"

def llm_chat(
    prompt: str = typer.Argument(..., help="Prompt to send to Llama 3.1 8B."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
    json_out: Path | None = typer.Option(None, help="Write response JSON to this path."),
) -> None:
    """Chat inference via Llama 3.1 8B (Cloudflare Workers AI). $0.060/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.inference(prompt=prompt)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    text_out = result.result or result.text or "(no response)"
    console.print(text_out)
    if json_out:
        d = result.model_dump()
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(d, indent=2), encoding="utf-8")
