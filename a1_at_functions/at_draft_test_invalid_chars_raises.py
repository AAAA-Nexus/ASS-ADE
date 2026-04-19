# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateagentid.py:28
# Component id: at.source.a1_at_functions.test_invalid_chars_raises
from __future__ import annotations

__version__ = "0.1.0"

def test_invalid_chars_raises(self) -> None:
    with pytest.raises(ValueError, match="invalid characters"):
        validate_agent_id("agent id with spaces")
    with pytest.raises(ValueError, match="invalid characters"):
        validate_agent_id("agent<script>")
