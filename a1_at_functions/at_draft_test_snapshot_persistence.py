# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_snapshot_persistence.py:7
# Component id: at.source.a1_at_functions.test_snapshot_persistence
from __future__ import annotations

__version__ = "0.1.0"

def test_snapshot_persistence(self, tmp_workspace: Path):
    h1 = FileHistory(str(tmp_workspace))
    h1.record("hello.py", "persistent content")

    # New history instance should find existing snapshots
    h2 = FileHistory(str(tmp_workspace))
    assert h2.depth("hello.py") == 1
    snaps = h2.list_snapshots("hello.py")
    assert snaps[0].content == "persistent content"
