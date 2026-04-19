# Extracted from C:/!ass-ade/tests/test_agent.py:54
# Component id: at.source.ass_ade.test_trim_noop_when_under_limit
from __future__ import annotations

__version__ = "0.1.0"

def test_trim_noop_when_under_limit(self):
    c = Conversation("system")
    c.add_user("hello")
    assert c.trim(max_messages=50) == 0
