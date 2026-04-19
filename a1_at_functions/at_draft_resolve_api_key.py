# Extracted from C:/!ass-ade/src/ass_ade/agent/providers.py:63
# Component id: at.source.ass_ade.resolve_api_key
from __future__ import annotations

__version__ = "0.1.0"

def resolve_api_key(self, config_key: str | None = None) -> str | None:
    """Resolve the API key: config override → env var → default."""
    if config_key:
        return config_key
    if self.api_key_env:
        env_val = os.getenv(self.api_key_env)
        if env_val:
            return env_val
    return self.api_key_default
