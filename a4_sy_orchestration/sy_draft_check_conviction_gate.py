# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/orchestrator.py:293
# Component id: sy.source.ass_ade.check_conviction_gate
__version__ = "0.1.0"

    def check_conviction_gate(self, tool_name: str, args: dict) -> bool:
        """Return True if the tool call should be BLOCKED due to low conviction.

        Only blocks destructive tools when conviction is below threshold.
        Fail-open: returns False (don't block) on any error.
        """
        if tool_name not in self._destructive_tools:
            return False
        try:
            conviction = self.wisdom.conviction if self._wisdom else 0.5
            if conviction < self._conviction_threshold and self.wisdom._audits > 0:
                _LOG.warning(
                    "Conviction gate: %s blocked (conviction=%.2f < %.2f)",
                    tool_name, conviction, self._conviction_threshold,
                )
                return True
        except Exception as exc:
            _LOG.debug("conviction gate check failed (fail-open): %s", exc)
        return False
