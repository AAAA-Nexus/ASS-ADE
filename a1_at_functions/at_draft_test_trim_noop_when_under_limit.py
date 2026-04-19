# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trim_noop_when_under_limit.py:7
# Component id: at.source.a1_at_functions.test_trim_noop_when_under_limit
from __future__ import annotations

__version__ = "0.1.0"

def test_trim_noop_when_under_limit(self):
    c = Conversation("system")
    c.add_user("hello")
    assert c.trim(max_messages=50) == 0
