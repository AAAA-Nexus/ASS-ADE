# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_history.py:26
# Component id: at.source.ass_ade.test_record_creates_snapshot
__version__ = "0.1.0"

    def test_record_creates_snapshot(self, history: FileHistory, tmp_workspace: Path):
        snap = history.record("hello.py", "print('hello')\n")
        assert snap.path == "hello.py"
        assert snap.sequence == 0
        assert snap.content == "print('hello')\n"
        assert snap.timestamp > 0
