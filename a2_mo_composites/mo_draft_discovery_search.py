# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:413
# Component id: mo.source.a2_mo_composites.discovery_search
from __future__ import annotations

__version__ = "0.1.0"

def discovery_search(self, capability: str, **kwargs: Any) -> DiscoveryResult:
    """/v1/discovery/search — search by capability, reputation-ranked. $0.060/call"""
    return self._post_model("/v1/discovery/search", DiscoveryResult, {"capability": capability, **kwargs})
