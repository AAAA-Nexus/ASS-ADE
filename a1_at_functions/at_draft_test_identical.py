# Extracted from C:/!ass-ade/tests/test_version_tracker.py:89
# Component id: at.source.ass_ade.test_identical
from __future__ import annotations

__version__ = "0.1.0"

def test_identical(self):
    body = "def foo(): pass"
    assert classify_change(body, body) == "none"
