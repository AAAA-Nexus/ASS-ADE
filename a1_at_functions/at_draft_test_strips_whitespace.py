# Extracted from C:/!ass-ade/tests/test_validation.py:21
# Component id: at.source.ass_ade.test_strips_whitespace
from __future__ import annotations

__version__ = "0.1.0"

def test_strips_whitespace(self) -> None:
    assert validate_agent_id("  agent-1  ") == "agent-1"
