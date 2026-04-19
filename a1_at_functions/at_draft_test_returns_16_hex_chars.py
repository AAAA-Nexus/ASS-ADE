# Extracted from C:/!ass-ade/tests/test_version_tracker.py:58
# Component id: at.source.ass_ade.test_returns_16_hex_chars
from __future__ import annotations

__version__ = "0.1.0"

def test_returns_16_hex_chars(self):
    h = content_hash("test")
    assert len(h) == 16
    assert all(c in "0123456789abcdef" for c in h)
