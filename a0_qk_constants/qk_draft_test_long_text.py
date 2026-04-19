# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testestimatetokens.py:22
# Component id: qk.source.a0_qk_constants.test_long_text
from __future__ import annotations

__version__ = "0.1.0"

def test_long_text(self):
    text = "The quick brown fox jumps over the lazy dog. " * 100
    result = estimate_tokens(text)
    # ~4500 chars / 3.7 ≈ ~1216 tokens
    assert 800 < result < 2000
