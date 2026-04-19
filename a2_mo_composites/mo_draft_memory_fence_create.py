# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:903
# Component id: mo.source.ass_ade.memory_fence_create
__version__ = "0.1.0"

    def memory_fence_create(self, namespace: str, **kwargs: Any) -> MemoryFence:
        """/v1/memory/fence — cross-tenant HMAC namespace boundary (MFN-100). $0.040/call"""
        return self._post_model("/v1/memory/fence", MemoryFence, {"namespace": namespace, **kwargs})
