# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a2_mo_composites/mo_draft_testconversation.py:8
# Component id: sy.source.a2_mo_composites.test_system_prompt
from __future__ import annotations

__version__ = "0.1.0"

def test_system_prompt(self):
    c = Conversation("You are helpful.")
    assert c.count() == 1
    assert c.messages[0].role == "system"
