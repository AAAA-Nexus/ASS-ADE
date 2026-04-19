# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_qualitygates.py:22
# Component id: at.source.ass_ade.gate_log
__version__ = "0.1.0"

    def gate_log(self) -> list[GateResult]:
        """Full log of gate results for this session."""
        return list(self._gate_log)
