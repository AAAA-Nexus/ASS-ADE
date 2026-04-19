# Extracted from C:/!ass-ade/tests/test_version_tracker.py:98
# Component id: at.source.ass_ade.test_minor_new_function
from __future__ import annotations

__version__ = "0.1.0"

def test_minor_new_function(self):
    old = "def foo(): pass"
    new = "def foo(): pass\ndef bar(): pass"
    assert classify_change(old, new) == "minor"
