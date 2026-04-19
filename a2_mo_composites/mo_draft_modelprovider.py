# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_modelprovider.py:7
# Component id: mo.source.a2_mo_composites.modelprovider
from __future__ import annotations

__version__ = "0.1.0"

class ModelProvider(Protocol):
    """Protocol for LLM providers."""

    def complete(self, request: CompletionRequest) -> CompletionResponse: ...
