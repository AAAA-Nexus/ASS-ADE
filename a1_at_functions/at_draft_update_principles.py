# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/wisdom.py:179
# Component id: at.source.ass_ade.update_principles
__version__ = "0.1.0"

    def update_principles(self, principles: list[str]) -> list[str]:
        for p in principles:
            if p not in self._principles:
                self._principles.append(p)
