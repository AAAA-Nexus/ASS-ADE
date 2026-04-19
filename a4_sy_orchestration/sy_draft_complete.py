# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_mcp_server_streaming.py:208
# Component id: sy.source.ass_ade.complete
__version__ = "0.1.0"

    def complete(self, request):
        idx = min(self._idx, len(self._responses) - 1)
        self._idx += 1
        return self._responses[idx]
