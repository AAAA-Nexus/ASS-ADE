# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:996
# Component id: mo.source.a2_mo_composites.memory_trim
from __future__ import annotations

__version__ = "0.1.0"

def memory_trim(self, context: list[dict], target_tokens: int, **kwargs: Any) -> MemoryTrimResult:
    """/v1/memory/trim — prune context window for cost efficiency (INF-815). $0.040/call"""
    return self._post_model("/v1/memory/trim", MemoryTrimResult, {"context": context, "target_tokens": target_tokens, **kwargs})
