# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:1199
# Component id: mo.source.ass_ade.routing_recommend
from __future__ import annotations

__version__ = "0.1.0"

def routing_recommend(self, task: str | None = None, *, prompt: str | None = None, **kwargs: Any) -> RoutingRecommend:
    """/v1/routing/recommend — map task to optimal model + routing tier. $0.020/call"""
    return self._post_model(
        "/v1/routing/recommend",
        RoutingRecommend,
        {"task": task or prompt or "", **kwargs},
    )
