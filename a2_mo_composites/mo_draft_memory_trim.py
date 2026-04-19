# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:1191
# Component id: mo.source.ass_ade.memory_trim
__version__ = "0.1.0"

    def memory_trim(self, context: list[dict], target_tokens: int, **kwargs: Any) -> MemoryTrimResult:
        """/v1/memory/trim — prune context window for cost efficiency (INF-815). $0.040/call"""
        return self._post_model("/v1/memory/trim", MemoryTrimResult, {"context": context, "target_tokens": target_tokens, **kwargs})
