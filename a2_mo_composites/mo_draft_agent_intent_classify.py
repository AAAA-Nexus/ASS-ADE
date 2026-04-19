# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:636
# Component id: mo.source.ass_ade.agent_intent_classify
from __future__ import annotations

__version__ = "0.1.0"

def agent_intent_classify(self, text: str, **kwargs: Any) -> IntentClassification:
    """/v1/agents/intent-classify — top-3 intents with confidence. $0.020/request"""
    return self._post_model("/v1/agents/intent-classify", IntentClassification, {"text": text, **kwargs})
