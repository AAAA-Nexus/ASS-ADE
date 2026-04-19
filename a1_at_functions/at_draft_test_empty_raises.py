# Extracted from C:/!ass-ade/tests/test_validation.py:24
# Component id: at.source.ass_ade.test_empty_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_raises(self) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        validate_agent_id("")
