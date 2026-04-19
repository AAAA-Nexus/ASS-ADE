# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_valid_ids.py:7
# Component id: at.source.a1_at_functions.test_valid_ids
from __future__ import annotations

__version__ = "0.1.0"

def test_valid_ids(self) -> None:
    assert validate_agent_id("agent-1") == "agent-1"
    assert validate_agent_id("13608") == "13608"
    assert validate_agent_id("my_agent.v2:latest") == "my_agent.v2:latest"
