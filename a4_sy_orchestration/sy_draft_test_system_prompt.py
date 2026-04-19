# Extracted from C:/!ass-ade/tests/test_agent.py:24
# Component id: sy.source.ass_ade.test_system_prompt
from __future__ import annotations

__version__ = "0.1.0"

def test_system_prompt(self):
    c = Conversation("You are helpful.")
    assert c.count() == 1
    assert c.messages[0].role == "system"
