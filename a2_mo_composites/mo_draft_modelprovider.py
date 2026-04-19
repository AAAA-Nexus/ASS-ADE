# Extracted from C:/!ass-ade/src/ass_ade/engine/provider.py:21
# Component id: mo.source.ass_ade.modelprovider
from __future__ import annotations

__version__ = "0.1.0"

class ModelProvider(Protocol):
    """Protocol for LLM providers."""

    def complete(self, request: CompletionRequest) -> CompletionResponse: ...
