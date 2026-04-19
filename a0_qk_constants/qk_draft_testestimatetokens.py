# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testestimatetokens.py:7
# Component id: qk.source.a0_qk_constants.testestimatetokens
from __future__ import annotations

__version__ = "0.1.0"

class TestEstimateTokens:
    def test_empty_string(self):
        assert estimate_tokens("") == 1  # min 1

    def test_short_text(self):
        result = estimate_tokens("hello world")
        assert result >= 1
        assert result <= 10

    def test_code_block(self):
        code = "def fibonacci(n: int) -> int:\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n"
        result = estimate_tokens(code)
        assert result >= 10
        assert result <= 100

    def test_long_text(self):
        text = "The quick brown fox jumps over the lazy dog. " * 100
        result = estimate_tokens(text)
        # ~4500 chars / 3.7 ≈ ~1216 tokens
        assert 800 < result < 2000

    def test_returns_int(self):
        assert isinstance(estimate_tokens("test"), int)
