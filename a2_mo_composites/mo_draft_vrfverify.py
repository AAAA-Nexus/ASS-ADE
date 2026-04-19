# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/models.py:209
# Component id: mo.source.ass_ade.vrfverify
__version__ = "0.1.0"

class VrfVerify(NexusModel):
    """/v1/vrf/verify-draw"""
    valid: bool | None = None
    draw_id: str | None = None
    proof: str | None = None
