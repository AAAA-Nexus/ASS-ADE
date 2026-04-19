# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testfilehistory.py:49
# Component id: at.source.ass_ade.test_list_snapshots
__version__ = "0.1.0"

    def test_list_snapshots(self, history: FileHistory):
        history.record("hello.py", "v1")
        history.record("hello.py", "v2")

        snaps = history.list_snapshots("hello.py")
        assert len(snaps) == 2
        assert snaps[0].content == "v1"
        assert snaps[1].content == "v2"
