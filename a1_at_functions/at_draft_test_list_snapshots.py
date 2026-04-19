# Extracted from C:/!ass-ade/tests/test_history.py:69
# Component id: at.source.ass_ade.test_list_snapshots
from __future__ import annotations

__version__ = "0.1.0"

def test_list_snapshots(self, history: FileHistory):
    history.record("hello.py", "v1")
    history.record("hello.py", "v2")

    snaps = history.list_snapshots("hello.py")
    assert len(snaps) == 2
    assert snaps[0].content == "v1"
    assert snaps[1].content == "v2"
