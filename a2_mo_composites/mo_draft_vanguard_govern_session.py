# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1304
# Component id: mo.source.ass_ade.vanguard_govern_session
__version__ = "0.1.0"

    def vanguard_govern_session(self, agent_id: str, session_key: str | None = None, *, wallet: str | None = None, **kwargs: Any) -> VanguardSessionResult:
        """POST /v1/vanguard/wallet/govern-session — UCAN wallet session control. $0.040/call"""
        return self._post_model("/v1/vanguard/wallet/govern-session", VanguardSessionResult, {"agent_id": agent_id, "session_key": session_key or wallet or "", **kwargs})
