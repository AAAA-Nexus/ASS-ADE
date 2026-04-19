# Extracted from C:/!ass-ade/src/ass_ade/engine/provider.py:306
# Component id: mo.source.ass_ade.providers
from __future__ import annotations

__version__ = "0.1.0"

def providers(self) -> dict[str, "ModelProvider"]:
    return dict(self._providers)
