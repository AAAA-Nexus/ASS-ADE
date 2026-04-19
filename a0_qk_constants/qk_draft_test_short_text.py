# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testestimatetokens.py:11
# Component id: qk.source.a0_qk_constants.test_short_text
from __future__ import annotations

__version__ = "0.1.0"

def test_short_text(self):
    result = estimate_tokens("hello world")
    assert result >= 1
    assert result <= 10
