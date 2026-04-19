# Extracted from C:/!ass-ade/tests/test_tokens.py:28
# Component id: qk.source.ass_ade.test_code_block
from __future__ import annotations

__version__ = "0.1.0"

def test_code_block(self):
    code = "def fibonacci(n: int) -> int:\n    if n <= 1:\n        return n\n    return fibonacci(n - 1) + fibonacci(n - 2)\n"
    result = estimate_tokens(code)
    assert result >= 10
    assert result <= 100
