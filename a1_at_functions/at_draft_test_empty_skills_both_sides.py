# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_empty_skills_both_sides.py:7
# Component id: at.source.a1_at_functions.test_empty_skills_both_sides
from __future__ import annotations

__version__ = "0.1.0"

def test_empty_skills_both_sides(self) -> None:
    local = self._make_card("Local")
    remote = self._make_card("Remote")
    result = negotiate(local, remote)
    assert not result.compatible
    assert result.shared_skills == []
