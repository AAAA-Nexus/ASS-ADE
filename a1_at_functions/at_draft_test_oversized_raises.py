# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateprompt.py:29
# Component id: at.source.a1_at_functions.test_oversized_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_oversized_raises(self) -> None:
    with pytest.raises(ValueError, match="exceeds"):
        validate_prompt("x" * 40_000)
