# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:776
# Component id: mo.source.ass_ade.authorize_action
__version__ = "0.1.0"

    def authorize_action(self, agent_id: str, action: str, delegation_depth: int = 0, **kwargs: Any) -> AuthorizeActionResult:
        """/v1/authorize/action — pre-action authorization gateway (OAP-100). $0.040/call"""
        return self._post_model("/v1/authorize/action", AuthorizeActionResult, {
            "agent_id": agent_id, "action": action, "delegation_depth": delegation_depth, **kwargs,
        })
