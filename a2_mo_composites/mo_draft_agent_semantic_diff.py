# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:632
# Component id: mo.source.ass_ade.agent_semantic_diff
__version__ = "0.1.0"

    def agent_semantic_diff(self, base: str, current: str, **kwargs: Any) -> SemanticDiff:
        """/v1/agents/semantic-diff — knowledge drift detection (Jaccard). $0.040/request"""
        return self._post_model("/v1/agents/semantic-diff", SemanticDiff, {"base": base, "current": current, **kwargs})
