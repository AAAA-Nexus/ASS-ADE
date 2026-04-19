# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_returns_16_hex_chars.py:7
# Component id: at.source.a1_at_functions.test_returns_16_hex_chars
from __future__ import annotations

__version__ = "0.1.0"

def test_returns_16_hex_chars(self):
    h = content_hash("test")
    assert len(h) == 16
    assert all(c in "0123456789abcdef" for c in h)
