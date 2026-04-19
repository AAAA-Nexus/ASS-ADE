# Extracted from C:/!ass-ade/tests/test_agent.py:29
# Component id: at.source.ass_ade.test_add_messages
from __future__ import annotations

__version__ = "0.1.0"

def test_add_messages(self):
    c = Conversation()
    c.add_user("hello")
    c.add_assistant(Message(role="assistant", content="hi"))
    assert c.count() == 2
