# Extracted from C:/!ass-ade/tests/test_validation.py:88
# Component id: at.source.ass_ade.testvalidatesessionid
from __future__ import annotations

__version__ = "0.1.0"

class TestValidateSessionId:
    def test_valid(self) -> None:
        assert validate_session_id("sess-abc-123") == "sess-abc-123"

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="must not be empty"):
            validate_session_id("")

    def test_too_long_raises(self) -> None:
        with pytest.raises(ValueError, match="exceeds 256"):
            validate_session_id("x" * 257)
