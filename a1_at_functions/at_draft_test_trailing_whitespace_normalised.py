# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trailing_whitespace_normalised.py:7
# Component id: at.source.a1_at_functions.test_trailing_whitespace_normalised
from __future__ import annotations

__version__ = "0.1.0"

def test_trailing_whitespace_normalised(self):
    assert content_hash("a  \nb  \n") == content_hash("a\nb")
