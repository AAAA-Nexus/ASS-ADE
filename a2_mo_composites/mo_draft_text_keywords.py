# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:937
# Component id: mo.source.a2_mo_composites.text_keywords
from __future__ import annotations

__version__ = "0.1.0"

def text_keywords(self, text: str, top_k: int = 10, **kwargs: Any) -> TextKeywords:
    """/v1/text/keywords — TF-IDF keyword extraction. $0.020/request"""
    return self._post_model("/v1/text/keywords", TextKeywords, {"text": text, "top_k": top_k, **kwargs})
