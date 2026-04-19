# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_no_shared_skills_incompatible.py:7
# Component id: at.source.a1_at_functions.test_no_shared_skills_incompatible
from __future__ import annotations

__version__ = "0.1.0"

def test_no_shared_skills_incompatible(self) -> None:
    local = self._make_card("Local", skills=[("s1", "Skill 1")])
    remote = self._make_card("Remote", skills=[("s2", "Skill 2")])
    result = negotiate(local, remote)
    assert not result.compatible
    assert result.shared_skills == []
