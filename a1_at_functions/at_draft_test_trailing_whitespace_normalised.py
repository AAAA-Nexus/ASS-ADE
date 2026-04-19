# Extracted from C:/!ass-ade/tests/test_version_tracker.py:55
# Component id: at.source.ass_ade.test_trailing_whitespace_normalised
from __future__ import annotations

__version__ = "0.1.0"

def test_trailing_whitespace_normalised(self):
    assert content_hash("a  \nb  \n") == content_hash("a\nb")
