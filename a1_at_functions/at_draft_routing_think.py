# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_routing_think.py:7
# Component id: at.source.a1_at_functions.routing_think
from __future__ import annotations

__version__ = "0.1.0"

def routing_think(self, query: str, **kwargs: Any) -> ThinkRoute:
    """/v1/routing/think — classify complexity → model tier (POP-1207). $0.040/call"""
    return self._post_model("/v1/routing/think", ThinkRoute, {"query": query, **kwargs})
