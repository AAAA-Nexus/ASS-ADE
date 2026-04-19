# Extracted from C:/!ass-ade/tests/test_validation.py:32
# Component id: at.source.ass_ade.test_too_long_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_too_long_raises(self) -> None:
    with pytest.raises(ValueError, match="exceeds 256"):
        validate_agent_id("a" * 257)
