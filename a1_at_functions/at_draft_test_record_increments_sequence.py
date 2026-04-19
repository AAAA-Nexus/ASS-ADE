# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testfilehistory.py:13
# Component id: at.source.ass_ade.test_record_increments_sequence
__version__ = "0.1.0"

    def test_record_increments_sequence(self, history: FileHistory):
        history.record("hello.py", "v1")
        snap = history.record("hello.py", "v2")
        assert snap.sequence == 1
