# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1308
# Component id: mo.source.ass_ade.vanguard_start_session
__version__ = "0.1.0"

    def vanguard_start_session(self, agent_id: str, **kwargs: Any) -> VanguardSessionResult:
        """POST /v1/vanguard/session/start — start a VANGUARD wallet session. $0.040/call"""
        return self._post_model("/v1/vanguard/session/start", VanguardSessionResult, {"agent_id": agent_id, **kwargs})
