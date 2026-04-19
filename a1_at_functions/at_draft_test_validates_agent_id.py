# Extracted from C:/!ass-ade/tests/test_workflows.py:102
# Component id: at.source.ass_ade.test_validates_agent_id
from __future__ import annotations

__version__ = "0.1.0"

def test_validates_agent_id(self) -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        trust_gate(_mock_client(), "")
