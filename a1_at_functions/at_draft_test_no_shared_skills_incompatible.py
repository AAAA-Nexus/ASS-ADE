# Extracted from C:/!ass-ade/tests/test_a2a.py:234
# Component id: at.source.ass_ade.test_no_shared_skills_incompatible
from __future__ import annotations

__version__ = "0.1.0"

def test_no_shared_skills_incompatible(self) -> None:
    local = self._make_card("Local", skills=[("s1", "Skill 1")])
    remote = self._make_card("Remote", skills=[("s2", "Skill 2")])
    result = negotiate(local, remote)
    assert not result.compatible
    assert result.shared_skills == []
