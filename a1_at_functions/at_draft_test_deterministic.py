# Extracted from C:/!ass-ade/tests/test_version_tracker.py:49
# Component id: at.source.ass_ade.test_deterministic
from __future__ import annotations

__version__ = "0.1.0"

def test_deterministic(self):
    assert content_hash("hello world") == content_hash("hello world")
