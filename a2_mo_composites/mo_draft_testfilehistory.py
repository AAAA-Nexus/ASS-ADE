# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testfilehistory.py:7
# Component id: mo.source.a2_mo_composites.testfilehistory
from __future__ import annotations

__version__ = "0.1.0"

class TestFileHistory:
    def test_record_creates_snapshot(self, history: FileHistory, tmp_workspace: Path):
        snap = history.record("hello.py", "print('hello')\n")
        assert snap.path == "hello.py"
        assert snap.sequence == 0
        assert snap.content == "print('hello')\n"
        assert snap.timestamp > 0

    def test_record_increments_sequence(self, history: FileHistory):
        history.record("hello.py", "v1")
        snap = history.record("hello.py", "v2")
        assert snap.sequence == 1

    def test_depth(self, history: FileHistory):
        assert history.depth("hello.py") == 0
        history.record("hello.py", "v1")
        assert history.depth("hello.py") == 1
        history.record("hello.py", "v2")
        assert history.depth("hello.py") == 2

    def test_undo_restores_content(self, history: FileHistory, tmp_workspace: Path):
        original = "print('hello')\n"
        history.record("hello.py", original)

        # Overwrite the file
        (tmp_workspace / "hello.py").write_text("print('goodbye')\n", encoding="utf-8")

        # Undo should restore
        snap = history.undo("hello.py")
        assert snap is not None
        assert snap.content == original
        assert (tmp_workspace / "hello.py").read_text(encoding="utf-8") == original

    def test_undo_no_history(self, history: FileHistory):
        assert history.undo("nonexistent.py") is None

    def test_undo_consumes_snapshot(self, history: FileHistory, tmp_workspace: Path):
        history.record("hello.py", "v1")
        history.record("hello.py", "v2")
        assert history.depth("hello.py") == 2

        history.undo("hello.py")
        assert history.depth("hello.py") == 1

    def test_list_snapshots(self, history: FileHistory):
        history.record("hello.py", "v1")
        history.record("hello.py", "v2")

        snaps = history.list_snapshots("hello.py")
        assert len(snaps) == 2
        assert snaps[0].content == "v1"
        assert snaps[1].content == "v2"

    def test_list_snapshots_empty(self, history: FileHistory):
        assert history.list_snapshots("nonexistent.py") == []

    def test_prune_limits_depth(self, history: FileHistory):
        for i in range(10):
            history.record("hello.py", f"version {i}")

        # max_depth is 5
        assert history.depth("hello.py") == 5

        # Should keep the latest 5
        snaps = history.list_snapshots("hello.py")
        assert snaps[0].content == "version 5"
        assert snaps[-1].content == "version 9"

    def test_multiple_files(self, history: FileHistory, tmp_workspace: Path):
        (tmp_workspace / "other.py").write_text("other", encoding="utf-8")
        history.record("hello.py", "h1")
        history.record("other.py", "o1")

        assert history.depth("hello.py") == 1
        assert history.depth("other.py") == 1

    def test_snapshot_persistence(self, tmp_workspace: Path):
        h1 = FileHistory(str(tmp_workspace))
        h1.record("hello.py", "persistent content")

        # New history instance should find existing snapshots
        h2 = FileHistory(str(tmp_workspace))
        assert h2.depth("hello.py") == 1
        snaps = h2.list_snapshots("hello.py")
        assert snaps[0].content == "persistent content"
