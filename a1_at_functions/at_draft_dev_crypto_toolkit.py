# Extracted from C:/!ass-ade/src/ass_ade/cli.py:3061
# Component id: at.source.ass_ade.dev_crypto_toolkit
from __future__ import annotations

__version__ = "0.1.0"

def dev_crypto_toolkit(
    data: str = typer.Argument(..., help="Data string to hash/proof."),
    config: Path | None = CONFIG_OPTION,
    allow_remote: bool = ALLOW_REMOTE_OPTION,
) -> None:
    """BLAKE3 + Merkle proof + nonce toolkit (DCM-1018). $0.020/call."""
    _, settings = _resolve_config(config)
    _require_remote_access(settings, allow_remote)
    try:
        with NexusClient(base_url=settings.nexus_base_url, timeout=settings.request_timeout_s, api_key=settings.nexus_api_key) as client:
            result = client.crypto_toolkit(data=data)
    except httpx.HTTPError as exc:
        _nexus_err(exc)
        return
    _print_json(result.model_dump())
