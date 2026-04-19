# Extracted from C:/!ass-ade/tests/test_validation.py:65
# Component id: at.source.ass_ade.test_oversized_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_oversized_raises(self) -> None:
    with pytest.raises(ValueError, match="exceeds"):
        validate_prompt("x" * 40_000)
