# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:262
# Component id: at.source.ass_ade.test_empty_skills_both_sides
__version__ = "0.1.0"

    def test_empty_skills_both_sides(self) -> None:
        local = self._make_card("Local")
        remote = self._make_card("Remote")
        result = negotiate(local, remote)
        assert not result.compatible
        assert result.shared_skills == []
