# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:964
# Component id: mo.source.a2_mo_composites.data_convert
from __future__ import annotations

__version__ = "0.1.0"

def data_convert(self, content: str, target_format: str, **kwargs: Any) -> dict:
    """/v1/data/convert — Convert text content to a target format. $0.020/request"""
    return self._post_raw("/v1/data/convert", {"content": content, "target_format": target_format, **kwargs})
