# Extracted from C:/!ass-ade/src/ass_ade/engine/provider.py:322
# Component id: mo.source.ass_ade.register
from __future__ import annotations

__version__ = "0.1.0"

def register(self, name: str, provider: "ModelProvider", models: list[str] | None = None) -> None:
    """Add a provider to the router at runtime."""
    self._providers[name] = provider
    if name not in self._fallback_order:
        self._fallback_order.append(name)
    for m in models or []:
        self._model_to_provider[m] = name
