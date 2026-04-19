# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/engine/provider.py:21
# Component id: mo.source.ass_ade.modelprovider
__version__ = "0.1.0"

class ModelProvider(Protocol):
    """Protocol for LLM providers."""

    def complete(self, request: CompletionRequest) -> CompletionResponse: ...
