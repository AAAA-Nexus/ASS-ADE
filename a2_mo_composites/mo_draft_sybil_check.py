# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:522
# Component id: mo.source.ass_ade.sybil_check
__version__ = "0.1.0"

    def sybil_check(self, actor: str | None = None, *, agent_id: str | None = None, **kwargs: Any) -> SybilCheckResult:
        """/v1/identity/sybil-check — sybil resistance check. $0.020/call"""
        return self._post_model("/v1/identity/sybil-check", SybilCheckResult, {"actor": actor or agent_id or "", **kwargs})
