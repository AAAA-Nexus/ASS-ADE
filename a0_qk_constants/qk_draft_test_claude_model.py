# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testcontextwindowfor.py:11
# Component id: qk.source.a0_qk_constants.test_claude_model
from __future__ import annotations

__version__ = "0.1.0"

def test_claude_model(self):
    assert context_window_for("claude-opus-4") == 200_000
