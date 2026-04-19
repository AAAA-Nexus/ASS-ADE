# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:608
# Component id: mo.source.ass_ade.discovery_search
__version__ = "0.1.0"

    def discovery_search(self, capability: str, **kwargs: Any) -> DiscoveryResult:
        """/v1/discovery/search — search by capability, reputation-ranked. $0.060/call"""
        return self._post_model("/v1/discovery/search", DiscoveryResult, {"capability": capability, **kwargs})
