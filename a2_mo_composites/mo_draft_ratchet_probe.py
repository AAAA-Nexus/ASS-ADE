# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:464
# Component id: mo.source.ass_ade.ratchet_probe
__version__ = "0.1.0"

    def ratchet_probe(self, session_ids: list[str], **kwargs: Any) -> RatchetProbeResult:
        """/v1/ratchet/probe — batch liveness check for up to 100 sessions. $0.008/call"""
        return self._post_model("/v1/ratchet/probe", RatchetProbeResult, {"session_ids": session_ids, **kwargs})
