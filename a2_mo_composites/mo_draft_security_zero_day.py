# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:692
# Component id: mo.source.ass_ade.security_zero_day
__version__ = "0.1.0"

    def security_zero_day(self, payload: dict, **kwargs: Any) -> ZeroDayResult:
        """/v1/security/zero-day — zero-day pattern detector for agent payloads. $0.040/request"""
        return self._post_model("/v1/security/zero-day", ZeroDayResult, {"payload": payload, **kwargs})
