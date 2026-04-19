# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_write_default_config.py:7
# Component id: at.source.a1_at_functions.write_default_config
from __future__ import annotations

__version__ = "0.1.0"

def write_default_config(
    path: Path | None = None,
    config: AssAdeConfig | None = None,
    *,
    overwrite: bool = False,
) -> Path:
    target = path or default_config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not overwrite:
        return target

    # Do not write sensitive API keys into the default config file.
    # This includes nexus_api_key AND every provider override's api_key.
    cfg = config or AssAdeConfig()
    payload_dict = cfg.model_dump(exclude={"nexus_api_key"})
    # Strip api_key from each provider override (secrets never go to disk)
    providers = payload_dict.get("providers") or {}
    for override in providers.values():
        if isinstance(override, dict):
            override.pop("api_key", None)
    import json as _json
    payload = _json.dumps(payload_dict, indent=2)
    target.write_text(f"{payload}\n", encoding="utf-8")
    # Restrict permissions to owner read/write only (0o600) so the config
    # directory is not world-readable on shared systems (OWASP A05).
    try:
        target.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except (OSError, NotImplementedError):
        pass  # Best-effort; Windows does not support POSIX permission bits.
    return target
