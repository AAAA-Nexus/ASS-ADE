# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testfilehistory.py:58
# Component id: at.source.ass_ade.test_list_snapshots_empty
__version__ = "0.1.0"

    def test_list_snapshots_empty(self, history: FileHistory):
        assert history.list_snapshots("nonexistent.py") == []
