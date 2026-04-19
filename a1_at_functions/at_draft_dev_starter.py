# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3040
# Component id: at.source.ass_ade.dev_starter
from __future__ import annotations

__version__ = "0.1.0"

def dev_starter(
    project_name: str = typer.Argument(..., help="Project name."),
    language: str = typer.Option("python", help="Language: python/rust/typescript."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Scaffold an agent project with x402 wiring (DEV-601). $0.040/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.dev_starter(project_name=project_name, language=language)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    console.print(f"Scaffolded: {result.project_name}  x402={result.x402_wired}")
    if result.files:
        _print_json(result.files)
