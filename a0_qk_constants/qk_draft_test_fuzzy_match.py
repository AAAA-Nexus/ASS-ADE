# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_testcontextwindowfor.py:20
# Component id: qk.source.a0_qk_constants.test_fuzzy_match
from __future__ import annotations

__version__ = "0.1.0"

def test_fuzzy_match(self):
    # Should match "llama-3.1-8b" as substring
    assert context_window_for("ollama/llama-3.1-8b") == 128_000
