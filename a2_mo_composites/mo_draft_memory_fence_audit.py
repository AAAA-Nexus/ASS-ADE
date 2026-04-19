# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:907
# Component id: mo.source.ass_ade.memory_fence_audit
__version__ = "0.1.0"

    def memory_fence_audit(self, fence_id: str) -> MemoryFenceAudit:
        """/v1/memory/fence/{id}/audit — access log + entry count (MFN-100). $0.020/call"""
        return self._get_model(f"/v1/memory/fence/{_pseg(fence_id, 'fence_id')}/audit", MemoryFenceAudit)
