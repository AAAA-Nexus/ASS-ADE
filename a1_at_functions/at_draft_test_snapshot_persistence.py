# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_history.py:101
# Component id: at.source.ass_ade.test_snapshot_persistence
__version__ = "0.1.0"

    def test_snapshot_persistence(self, tmp_workspace: Path):
        h1 = FileHistory(str(tmp_workspace))
        h1.record("hello.py", "persistent content")

        # New history instance should find existing snapshots
        h2 = FileHistory(str(tmp_workspace))
        assert h2.depth("hello.py") == 1
        snaps = h2.list_snapshots("hello.py")
        assert snaps[0].content == "persistent content"
