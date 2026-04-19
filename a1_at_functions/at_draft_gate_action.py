# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/wisdom.py:247
# Component id: at.source.ass_ade.gate_action
__version__ = "0.1.0"

    def gate_action(self, action: str, cycle_state: dict) -> tuple[bool, str]:
        self.run_audit(cycle_state)
        if self.is_confident:
            return (True, "conviction_met")
        return (
            False,
            f"conviction {self._conviction:.2f} below required {self._conviction_required:.2f}",
        )
