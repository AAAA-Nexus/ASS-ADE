# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testfilehistory.py:61
# Component id: at.source.ass_ade.test_prune_limits_depth
__version__ = "0.1.0"

    def test_prune_limits_depth(self, history: FileHistory):
        for i in range(10):
            history.record("hello.py", f"version {i}")

        # max_depth is 5
        assert history.depth("hello.py") == 5

        # Should keep the latest 5
        snaps = history.list_snapshots("hello.py")
        assert snaps[0].content == "version 5"
        assert snaps[-1].content == "version 9"
