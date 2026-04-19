# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testcontextwindowfor.py:14
# Component id: qk.source.a0_qk_constants.test_unknown_model
from __future__ import annotations

__version__ = "0.1.0"

def test_unknown_model(self):
    assert context_window_for("totally-unknown-model") == DEFAULT_CONTEXT_WINDOW
