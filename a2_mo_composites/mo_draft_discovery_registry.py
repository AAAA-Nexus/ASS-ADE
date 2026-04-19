# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:616
# Component id: mo.source.ass_ade.discovery_registry
__version__ = "0.1.0"

    def discovery_registry(self, **kwargs: Any) -> AgentRegistry:
        """/v1/discovery/registry — browse all registered agents. $0.020/call"""
        return self._get_model("/v1/discovery/registry", AgentRegistry, **kwargs)
