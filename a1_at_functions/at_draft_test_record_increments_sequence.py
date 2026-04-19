# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_record_increments_sequence.py:7
# Component id: at.source.a1_at_functions.test_record_increments_sequence
from __future__ import annotations

__version__ = "0.1.0"

def test_record_increments_sequence(self, history: FileHistory):
    history.record("hello.py", "v1")
    snap = history.record("hello.py", "v2")
    assert snap.sequence == 1
