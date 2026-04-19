# Extracted from C:/!ass-ade/src/ass_ade/commands/a2a.py:133
# Component id: at.source.ass_ade.a2a_discover
from __future__ import annotations

__version__ = "0.1.0"

def a2a_discover(
    capability: Annotated[str, typer.Argument(help="Capability to search for.")],
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """Discover agents matching a capability."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)

    try:
        with NexusClient(
            base_url=settings.nexus_base_url,
            timeout=settings.request_timeout_s,
            api_key=settings.nexus_api_key,
        ) as client:
            results = client.discovery_search(capability=capability)
            # Convert to JSON-serializable format
            if hasattr(results, 'model_dump'):
                results_dict = results.model_dump()
            else:
                results_dict = results
            console.print(json.dumps(results_dict, indent=2), markup=False)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
