# Extracted from C:/!ass-ade/tests/test_a2a.py:298
# Component id: at.source.ass_ade.test_agent_card_name_validation
from __future__ import annotations

__version__ = "0.1.0"

def test_agent_card_name_validation(self) -> None:
    with pytest.raises(Exception):
        A2AAgentCard(name="")
