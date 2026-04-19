# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:702
# Component id: mo.source.ass_ade.security_shield
__version__ = "0.1.0"

    def security_shield(self, payload: dict, **kwargs: Any) -> ShieldResult:
        """/v1/security/shield — payload sanitization layer for agentic tool calls. $0.040/request"""
        return self._post_model("/v1/security/shield", ShieldResult, {"payload": payload, **kwargs})
