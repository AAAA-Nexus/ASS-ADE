# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_is_available.py:7
# Component id: at.source.a1_at_functions.is_available
from __future__ import annotations

__version__ = "0.1.0"

def is_available(self, config_key: str | None = None) -> bool:
    """True if this provider has auth (or is local + reachable)."""
    if self.local:
        return True
    return self.resolve_api_key(config_key) is not None
