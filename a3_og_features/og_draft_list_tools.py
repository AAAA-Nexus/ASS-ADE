# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_toolregistry.py:19
# Component id: og.source.a3_og_features.list_tools
from __future__ import annotations

__version__ = "0.1.0"

def list_tools(self) -> list[str]:
    return sorted(self._tools)
