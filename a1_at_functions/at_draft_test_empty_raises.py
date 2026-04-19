# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidatesessionid.py:11
# Component id: at.source.a1_at_functions.test_empty_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_raises(self) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        validate_session_id("")
