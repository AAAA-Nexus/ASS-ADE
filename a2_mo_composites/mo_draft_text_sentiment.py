# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:941
# Component id: mo.source.a2_mo_composites.text_sentiment
from __future__ import annotations

__version__ = "0.1.0"

def text_sentiment(self, text: str, **kwargs: Any) -> TextSentiment:
    """/v1/text/sentiment — positive / negative / neutral. $0.020/request"""
    return self._post_model("/v1/text/sentiment", TextSentiment, {"text": text, **kwargs})
