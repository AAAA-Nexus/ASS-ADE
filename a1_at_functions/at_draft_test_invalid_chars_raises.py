# Extracted from C:/!ass-ade/tests/test_validation.py:36
# Component id: at.source.ass_ade.test_invalid_chars_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_invalid_chars_raises(self) -> None:
    with pytest.raises(ValueError, match="invalid characters"):
        validate_agent_id("agent id with spaces")
    with pytest.raises(ValueError, match="invalid characters"):
        validate_agent_id("agent<script>")
