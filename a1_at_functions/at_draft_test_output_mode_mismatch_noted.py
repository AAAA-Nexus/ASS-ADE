# Extracted from C:/!ass-ade/tests/test_a2a.py:256
# Component id: at.source.ass_ade.test_output_mode_mismatch_noted
from __future__ import annotations

__version__ = "0.1.0"

def test_output_mode_mismatch_noted(self) -> None:
    local = self._make_card("Local", skills=[("s1", "S1")], input_modes=["text/plain"])
    remote = self._make_card("Remote", skills=[("s1", "S1")], output_modes=["application/pdf"])
    result = negotiate(local, remote)
    assert any("Output format mismatch" in n for n in result.notes)
