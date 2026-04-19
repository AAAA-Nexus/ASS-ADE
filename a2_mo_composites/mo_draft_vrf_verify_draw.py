# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_nexusclient.py:295
# Component id: mo.source.a2_mo_composites.vrf_verify_draw
from __future__ import annotations

__version__ = "0.1.0"

def vrf_verify_draw(self, draw_id: str, **kwargs: Any) -> VrfVerify:
    """/v1/vrf/verify-draw — verify a prior draw. Included with draw"""
    return self._post_model("/v1/vrf/verify-draw", VrfVerify, {"draw_id": draw_id, **kwargs})
