# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1136
# Component id: mo.source.ass_ade.text_sentiment
from __future__ import annotations

__version__ = "0.1.0"

def text_sentiment(self, text: str, **kwargs: Any) -> TextSentiment:
    """/v1/text/sentiment — positive / negative / neutral. $0.020/request"""
    return self._post_model("/v1/text/sentiment", TextSentiment, {"text": text, **kwargs})
