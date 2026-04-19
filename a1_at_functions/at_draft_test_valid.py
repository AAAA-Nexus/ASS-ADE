# Extracted from C:/!ass-ade/tests/test_validation.py:89
# Component id: at.source.ass_ade.test_valid
from __future__ import annotations

__version__ = "0.1.0"

def test_valid(self) -> None:
    assert validate_session_id("sess-abc-123") == "sess-abc-123"
