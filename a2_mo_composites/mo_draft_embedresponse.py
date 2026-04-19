# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:120
# Component id: mo.source.ass_ade.embedresponse
__version__ = "0.1.0"

class EmbedResponse(NexusModel):
    """/v1/embed — HELIX compressed embedding"""
    embedding: list[float] | None = Field(default=None)
    compressed: str | None = None    # base64 HELIX blob
    dimensions: int | None = None
    latency_ms: float | None = None
