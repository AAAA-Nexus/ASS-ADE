# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_filehistory.py:131
# Component id: at.source.ass_ade.depth
__version__ = "0.1.0"

    def depth(self, rel_path: str) -> int:
        """Number of undo steps available for a file."""
        snap_dir = self._snapshot_dir(rel_path)
        if not snap_dir.exists():
            return 0
        return len(list(snap_dir.glob("*.snapshot")))
