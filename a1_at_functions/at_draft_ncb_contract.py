# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/agent/tca.py:107
# Component id: at.source.ass_ade.ncb_contract
__version__ = "0.1.0"

    def ncb_contract(self, target_path: str | Path) -> bool:
        """Return True if NCB contract is satisfied (file was read before writing)."""
        return self.check_freshness(target_path).fresh
