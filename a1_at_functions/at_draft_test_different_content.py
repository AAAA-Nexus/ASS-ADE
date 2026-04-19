# Extracted from C:/!ass-ade/tests/test_version_tracker.py:52
# Component id: at.source.ass_ade.test_different_content
from __future__ import annotations

__version__ = "0.1.0"

def test_different_content(self):
    assert content_hash("foo") != content_hash("bar")
