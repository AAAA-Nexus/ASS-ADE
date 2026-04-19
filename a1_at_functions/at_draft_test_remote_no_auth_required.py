# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:269
# Component id: at.source.ass_ade.test_remote_no_auth_required
__version__ = "0.1.0"

    def test_remote_no_auth_required(self) -> None:
        local = self._make_card("Local", skills=[("s1", "S1")])
        remote = self._make_card("Remote", skills=[("s1", "S1")])
        result = negotiate(local, remote)
        assert result.auth_compatible
