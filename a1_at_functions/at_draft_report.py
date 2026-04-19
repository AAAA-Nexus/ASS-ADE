# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_trustverificationgate.py:54
# Component id: at.source.ass_ade.report
__version__ = "0.1.0"

    def report(self) -> dict:
        return {
            "engine": "trust_gate",
            "checks": self._checks,
            "denied": self._denied,
        }
