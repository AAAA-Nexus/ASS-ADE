# Extracted from C:/!ass-ade/tests/test_validation.py:16
# Component id: at.source.ass_ade.test_valid_ids
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_ids(self) -> None:
    assert validate_agent_id("agent-1") == "agent-1"
    assert validate_agent_id("13608") == "13608"
    assert validate_agent_id("my_agent.v2:latest") == "my_agent.v2:latest"
