# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_tcaengine.py:70
# Component id: mo.source.ass_ade.ncb_contract
__version__ = "0.1.0"

    def ncb_contract(self, target_path: str | Path) -> bool:
        """Return True if NCB contract is satisfied (file was read before writing)."""
        return self.check_freshness(target_path).fresh
