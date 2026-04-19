# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_bitnet_models.py:7
# Component id: at.source.a1_at_functions.bitnet_models
from __future__ import annotations

__version__ = "0.1.0"

def bitnet_models(
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """List available 1.58-bit BitNet models. Free."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.bitnet_models()
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    table = Table(title="BitNet 1.58-bit Models")
    table.add_column("ID")
    table.add_column("Provider")
    table.add_column("Params (B)")
    table.add_column("Memory (GB)")
    table.add_column("Status")
    for m in result.models:
        table.add_row(m.id or "", m.provider or "", str(m.params_b or ""), str(m.memory_gb or ""), m.status or "")
    console.print(table)
