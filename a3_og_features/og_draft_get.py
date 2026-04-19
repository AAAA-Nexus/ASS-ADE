# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a3_og_features/og_draft_toolregistry.py:16
# Component id: og.source.a3_og_features.get
from __future__ import annotations

__version__ = "0.1.0"

def get(self, name: str) -> Tool | None:
    return self._tools.get(name)
