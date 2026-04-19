# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidatesessionid.py:15
# Component id: at.source.a1_at_functions.test_too_long_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_too_long_raises(self) -> None:
    with pytest.raises(ValueError, match="exceeds 256"):
        validate_session_id("x" * 257)
