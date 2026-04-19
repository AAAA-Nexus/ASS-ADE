# Extracted from C:/!ass-ade/tests/test_version_tracker.py:103
# Component id: at.source.ass_ade.test_major_removed_function
from __future__ import annotations

__version__ = "0.1.0"

def test_major_removed_function(self):
    old = "def foo(): pass\ndef bar(): pass"
    new = "def foo(): pass"
    assert classify_change(old, new) == "major"
