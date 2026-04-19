# Extracted from C:/!ass-ade/tests/test_routing.py:37
# Component id: at.source.ass_ade.test_long_text_adds_complexity
from __future__ import annotations

__version__ = "0.1.0"

def test_long_text_adds_complexity(self):
    short = classify_complexity("Fix the bug")
    long_ = classify_complexity("Fix the bug " + "detailed context " * 100)
    assert long_ > short
