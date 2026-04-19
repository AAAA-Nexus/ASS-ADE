# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:490
# Component id: mo.source.ass_ade.vrf_verify_draw
__version__ = "0.1.0"

    def vrf_verify_draw(self, draw_id: str, **kwargs: Any) -> VrfVerify:
        """/v1/vrf/verify-draw — verify a prior draw. Included with draw"""
        return self._post_model("/v1/vrf/verify-draw", VrfVerify, {"draw_id": draw_id, **kwargs})
