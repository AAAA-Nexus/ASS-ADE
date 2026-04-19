# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:437
# Component id: mo.source.a2_mo_composites.agent_semantic_diff
from __future__ import annotations

__version__ = "0.1.0"

def agent_semantic_diff(self, base: str, current: str, **kwargs: Any) -> SemanticDiff:
    """/v1/agents/semantic-diff — knowledge drift detection (Jaccard). $0.040/request"""
    return self._post_model("/v1/agents/semantic-diff", SemanticDiff, {"base": base, "current": current, **kwargs})
