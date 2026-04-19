# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:849
# Component id: mo.source.ass_ade.federation_portability
__version__ = "0.1.0"

    def federation_portability(self, from_platform: str, to_platform: str, **kwargs: Any) -> PortabilityCheck:
        """/v1/federation/portability — cross-platform capability portability (AIF-102). $0.020/call"""
        return self._post_model("/v1/federation/portability", PortabilityCheck, {
            "from_platform": from_platform, "to_platform": to_platform, **kwargs,
        })
