# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1195
# Component id: mo.source.ass_ade.routing_think
__version__ = "0.1.0"

    def routing_think(self, query: str, **kwargs: Any) -> ThinkRoute:
        """/v1/routing/think — classify complexity → model tier (POP-1207). $0.040/call"""
        return self._post_model("/v1/routing/think", ThinkRoute, {"query": query, **kwargs})
