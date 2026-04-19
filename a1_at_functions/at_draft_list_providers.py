# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_list_providers.py:7
# Component id: at.source.a1_at_functions.list_providers
from __future__ import annotations

__version__ = "0.1.0"

def list_providers() -> list[str]:
    """All provider names known to the catalog."""
    return list(FREE_PROVIDERS.keys())
