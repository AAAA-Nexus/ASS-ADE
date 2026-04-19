# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:432
# Component id: mo.source.ass_ade.embed
__version__ = "0.1.0"

    def embed(self, values: list[float], **kwargs: Any) -> EmbedResponse:
        """/v1/embed — HELIX compressed embedding. $0.040/request"""
        return self._post_model("/v1/embed", EmbedResponse, {"values": values, **kwargs})
