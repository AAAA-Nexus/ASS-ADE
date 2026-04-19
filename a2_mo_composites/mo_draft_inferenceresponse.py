# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:110
# Component id: mo.source.ass_ade.inferenceresponse
__version__ = "0.1.0"

class InferenceResponse(NexusModel):
    """/v1/inference and /v1/embed"""
    result: str | None = None
    text: str | None = None          # alias used by some versions
    tokens_used: int | None = None
    model: str | None = None
    latency_ms: float | None = None
    helix_metadata: dict | None = None
