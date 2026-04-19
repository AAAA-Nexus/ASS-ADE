# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testfilehistory.py:38
# Component id: at.source.ass_ade.test_undo_no_history
__version__ = "0.1.0"

    def test_undo_no_history(self, history: FileHistory):
        assert history.undo("nonexistent.py") is None
