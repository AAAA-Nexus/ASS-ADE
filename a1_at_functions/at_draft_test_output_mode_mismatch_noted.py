# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_output_mode_mismatch_noted.py:7
# Component id: at.source.a1_at_functions.test_output_mode_mismatch_noted
from __future__ import annotations

__version__ = "0.1.0"

def test_output_mode_mismatch_noted(self) -> None:
    local = self._make_card("Local", skills=[("s1", "S1")], input_modes=["text/plain"])
    remote = self._make_card("Remote", skills=[("s1", "S1")], output_modes=["application/pdf"])
    result = negotiate(local, remote)
    assert any("Output format mismatch" in n for n in result.notes)
