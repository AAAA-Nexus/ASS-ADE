# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_completionrequest.py:7
# Component id: mo.source.a2_mo_composites.completionrequest
from __future__ import annotations

__version__ = "0.1.0"

class CompletionRequest(BaseModel):
    """Model completion request."""

    messages: list[Message]
    tools: list[ToolSchema] = Field(default_factory=list)
    temperature: float = 0.0
    max_tokens: int = 4096
    model: str | None = None
