# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:933
# Component id: mo.source.a2_mo_composites.text_summarize
from __future__ import annotations

__version__ = "0.1.0"

def text_summarize(self, text: str, **kwargs: Any) -> TextSummary:
    """/v1/text/summarize — 1-3 sentence extractive summary. $0.040/request"""
    return self._post_model("/v1/text/summarize", TextSummary, {"text": text, **kwargs})
