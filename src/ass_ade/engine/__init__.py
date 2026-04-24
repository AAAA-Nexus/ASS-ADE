"""ASS-ADE engine — LLM routing and codebase rebuild pipeline."""

from ass_ade.engine.rebuild.orchestrator import rebuild_project, render_rebuild_summary

# LLM routing components require the full ass_ade package installation.
# Guard these imports so the rebuild subpackage stays usable standalone.
try:
    from ass_ade.engine.provider import ModelProvider, NexusProvider, OpenAICompatibleProvider
    from ass_ade.engine.router import build_provider
    from ass_ade.engine.types import (
        CompletionRequest,
        CompletionResponse,
        Message,
        ToolCallRequest,
        ToolSchema,
    )
    _FULL_ENGINE = True
except ImportError:
    _FULL_ENGINE = False

__all__ = [
    "rebuild_project",
    "render_rebuild_summary",
]
if _FULL_ENGINE:
    __all__ += [
        "CompletionRequest",
        "CompletionResponse",
        "Message",
        "ModelProvider",
        "NexusProvider",
        "OpenAICompatibleProvider",
        "ToolCallRequest",
        "ToolSchema",
        "build_provider",
    ]
