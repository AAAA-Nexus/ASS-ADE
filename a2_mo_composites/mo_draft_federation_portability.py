# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:654
# Component id: mo.source.a2_mo_composites.federation_portability
from __future__ import annotations

__version__ = "0.1.0"

def federation_portability(self, from_platform: str, to_platform: str, **kwargs: Any) -> PortabilityCheck:
    """/v1/federation/portability — cross-platform capability portability (AIF-102). $0.020/call"""
    return self._post_model("/v1/federation/portability", PortabilityCheck, {
        "from_platform": from_platform, "to_platform": to_platform, **kwargs,
    })
