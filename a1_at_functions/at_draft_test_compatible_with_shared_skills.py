# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_compatible_with_shared_skills.py:7
# Component id: at.source.a1_at_functions.test_compatible_with_shared_skills
from __future__ import annotations

__version__ = "0.1.0"

def test_compatible_with_shared_skills(self) -> None:
    local = self._make_card("Local", skills=[("s1", "Skill 1"), ("s2", "Skill 2")])
    remote = self._make_card("Remote", skills=[("s2", "Skill 2"), ("s3", "Skill 3")])
    result = negotiate(local, remote)
    assert result.compatible
    assert result.shared_skills == ["s2"]
    assert result.local_only == ["s1"]
    assert result.remote_only == ["s3"]
