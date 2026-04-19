# Extracted from C:/!ass-ade/src/ass_ade/agent/providers.py:80
# Component id: at.source.ass_ade.is_available
from __future__ import annotations

__version__ = "0.1.0"

def is_available(self, config_key: str | None = None) -> bool:
    """True if this provider has auth (or is local + reachable)."""
    if self.local:
        return True
    return self.resolve_api_key(config_key) is not None
