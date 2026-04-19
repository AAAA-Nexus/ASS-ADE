# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:612
# Component id: mo.source.ass_ade.discovery_recommend
from __future__ import annotations

__version__ = "0.1.0"

def discovery_recommend(self, task: str, **kwargs: Any) -> DiscoveryResult:
    """/v1/discovery/recommend — AI-ranked recommendations from task description. $0.040/call"""
    return self._post_model("/v1/discovery/recommend", DiscoveryResult, {"task": task, **kwargs})
