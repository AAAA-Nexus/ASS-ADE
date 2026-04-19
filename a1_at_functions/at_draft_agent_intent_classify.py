# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_agent_intent_classify.py:7
# Component id: at.source.a1_at_functions.agent_intent_classify
from __future__ import annotations

__version__ = "0.1.0"

def agent_intent_classify(self, text: str, **kwargs: Any) -> IntentClassification:
    """/v1/agents/intent-classify — top-3 intents with confidence. $0.020/request"""
    return self._post_model("/v1/agents/intent-classify", IntentClassification, {"text": text, **kwargs})
