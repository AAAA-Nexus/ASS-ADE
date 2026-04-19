# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_record_creates_snapshot.py:7
# Component id: at.source.a1_at_functions.test_record_creates_snapshot
from __future__ import annotations

__version__ = "0.1.0"

def test_record_creates_snapshot(self, history: FileHistory, tmp_workspace: Path):
    snap = history.record("hello.py", "print('hello')\n")
    assert snap.path == "hello.py"
    assert snap.sequence == 0
    assert snap.content == "print('hello')\n"
    assert snap.timestamp > 0
