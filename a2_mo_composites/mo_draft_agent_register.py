# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:622
# Component id: mo.source.ass_ade.agent_register
__version__ = "0.1.0"

    def agent_register(self, agent_id: int, name: str, capabilities: list[str], endpoint: str, **kwargs: Any) -> AgentRegistration:
        """POST /v1/agents/register — agent_id must be a multiple of G_18 (324). Free"""
        return self._post_model("/v1/agents/register", AgentRegistration, {
            "agent_id": agent_id, "name": name, "capabilities": capabilities, "endpoint": endpoint, **kwargs,
        })
