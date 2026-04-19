# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_trim.py:7
# Component id: at.source.a1_at_functions.test_trim
from __future__ import annotations

__version__ = "0.1.0"

def test_trim(self):
    c = Conversation("system")
    for i in range(60):
        c.add_user(f"msg {i}")
    assert c.count() == 61  # 1 system + 60 user
    removed = c.trim(max_messages=10)
    assert removed == 51
    assert c.count() == 10
    # System prompt preserved
    assert c.messages[0].role == "system"
