# Extracted from C:/!ass-ade/src/ass_ade/nexus/client.py:486
# Component id: mo.source.ass_ade.vrf_draw
from __future__ import annotations

__version__ = "0.1.0"

def vrf_draw(self, range_min: int, range_max: int, count: int = 1, **kwargs: Any) -> VrfDraw:
    """/v1/vrf/draw — VRF random draw with on-chain proof. $0.01 + 0.5% of pot"""
    return self._post_model("/v1/vrf/draw", VrfDraw, {"range_min": range_min, "range_max": range_max, "count": count, **kwargs})
