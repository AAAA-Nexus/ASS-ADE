# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:281
# Component id: mo.source.ass_ade.get_agent_card
__version__ = "0.1.0"

    def get_agent_card(self) -> AgentCard:
        """/.well-known/agent.json — A2A capability manifest, free"""
        return self._get_model("/.well-known/agent.json", AgentCard)
