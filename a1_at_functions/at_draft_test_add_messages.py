# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_add_messages.py:7
# Component id: at.source.a1_at_functions.test_add_messages
from __future__ import annotations

__version__ = "0.1.0"

def test_add_messages(self):
    c = Conversation()
    c.add_user("hello")
    c.add_assistant(Message(role="assistant", content="hi"))
    assert c.count() == 2
