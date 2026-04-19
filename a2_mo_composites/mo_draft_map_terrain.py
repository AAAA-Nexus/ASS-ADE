# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:944
# Component id: mo.source.ass_ade.map_terrain
__version__ = "0.1.0"

    def map_terrain(self, required_capabilities: list, **kwargs: Any) -> dict:
        """Capability gap detection. Verdict PROCEED or HALT_AND_INVENT."""
        try:
            return self._post_raw(
                "/v1/map/terrain",
                {"required_capabilities": required_capabilities, **kwargs},
            )
        except Exception:
            return {
                "verdict": "PROCEED",
                "missing": [],
                "fallback": "local_assume_present",
            }
