# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:378
# Component id: mo.source.ass_ade.intentclassification
__version__ = "0.1.0"

class IntentClassification(NexusModel):
    """/v1/agents/intent-classify"""
    top_intents: list[dict] = Field(default_factory=list)   # [{intent, confidence}]
    primary_intent: str | None = None
