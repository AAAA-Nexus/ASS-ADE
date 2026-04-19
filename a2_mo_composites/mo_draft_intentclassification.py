# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_intentclassification.py:7
# Component id: mo.source.a2_mo_composites.intentclassification
from __future__ import annotations

__version__ = "0.1.0"

class IntentClassification(NexusModel):
    """/v1/agents/intent-classify"""
    top_intents: list[dict] = Field(default_factory=list)   # [{intent, confidence}]
    primary_intent: str | None = None
