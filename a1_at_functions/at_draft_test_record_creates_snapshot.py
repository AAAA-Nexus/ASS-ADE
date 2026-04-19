# Extracted from C:/!ass-ade/tests/test_history.py:26
# Component id: at.source.ass_ade.test_record_creates_snapshot
from __future__ import annotations

__version__ = "0.1.0"

def test_record_creates_snapshot(self, history: FileHistory, tmp_workspace: Path):
    snap = history.record("hello.py", "print('hello')\n")
    assert snap.path == "hello.py"
    assert snap.sequence == 0
    assert snap.content == "print('hello')\n"
    assert snap.timestamp > 0
