# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testvalidateagentid.py:13
# Component id: at.source.a1_at_functions.test_strips_whitespace
from __future__ import annotations

__version__ = "0.1.0"

def test_strips_whitespace(self) -> None:
    assert validate_agent_id("  agent-1  ") == "agent-1"
