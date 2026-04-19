# Extracted from C:/!ass-ade/tests/test_history.py:33
# Component id: at.source.ass_ade.test_record_increments_sequence
from __future__ import annotations

__version__ = "0.1.0"

def test_record_increments_sequence(self, history: FileHistory):
    history.record("hello.py", "v1")
    snap = history.record("hello.py", "v2")
    assert snap.sequence == 1
