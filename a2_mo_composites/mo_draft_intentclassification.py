# Extracted from C:/!ass-ade/src/ass_ade/nexus/models.py:378
# Component id: mo.source.ass_ade.intentclassification
from __future__ import annotations

__version__ = "0.1.0"

class IntentClassification(NexusModel):
    """/v1/agents/intent-classify"""
    top_intents: list[dict] = Field(default_factory=list)   # [{intent, confidence}]
    primary_intent: str | None = None
