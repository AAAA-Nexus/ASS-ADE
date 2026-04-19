# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_a2a.py:208
# Component id: mo.source.ass_ade.testnegotiate
__version__ = "0.1.0"

class TestNegotiate:
    def _make_card(
        self,
        name: str = "Agent",
        skills: list[tuple[str, str]] | None = None,
        auth_schemes: list[str] | None = None,
        input_modes: list[str] | None = None,
        output_modes: list[str] | None = None,
    ) -> A2AAgentCard:
        return A2AAgentCard(
            name=name,
            skills=[A2ASkill(id=sid, name=sn) for sid, sn in (skills or [])],
            authentication=A2AAuthentication(schemes=auth_schemes or []),
            defaultInputModes=input_modes or ["text/plain"],
            defaultOutputModes=output_modes or ["text/plain"],
        )

    def test_compatible_with_shared_skills(self) -> None:
        local = self._make_card("Local", skills=[("s1", "Skill 1"), ("s2", "Skill 2")])
        remote = self._make_card("Remote", skills=[("s2", "Skill 2"), ("s3", "Skill 3")])
        result = negotiate(local, remote)
        assert result.compatible
        assert result.shared_skills == ["s2"]
        assert result.local_only == ["s1"]
        assert result.remote_only == ["s3"]

    def test_no_shared_skills_incompatible(self) -> None:
        local = self._make_card("Local", skills=[("s1", "Skill 1")])
        remote = self._make_card("Remote", skills=[("s2", "Skill 2")])
        result = negotiate(local, remote)
        assert not result.compatible
        assert result.shared_skills == []

    def test_auth_mismatch(self) -> None:
        local = self._make_card("Local", skills=[("s1", "S1")], auth_schemes=["api_key"])
        remote = self._make_card("Remote", skills=[("s1", "S1")], auth_schemes=["bearer"])
        result = negotiate(local, remote)
        assert not result.compatible
        assert not result.auth_compatible
        assert any("Auth mismatch" in n for n in result.notes)

    def test_auth_compatible(self) -> None:
        local = self._make_card("Local", skills=[("s1", "S1")], auth_schemes=["bearer"])
        remote = self._make_card("Remote", skills=[("s1", "S1")], auth_schemes=["bearer"])
        result = negotiate(local, remote)
        assert result.compatible
        assert result.auth_compatible

    def test_output_mode_mismatch_noted(self) -> None:
        local = self._make_card("Local", skills=[("s1", "S1")], input_modes=["text/plain"])
        remote = self._make_card("Remote", skills=[("s1", "S1")], output_modes=["application/pdf"])
        result = negotiate(local, remote)
        assert any("Output format mismatch" in n for n in result.notes)

    def test_empty_skills_both_sides(self) -> None:
        local = self._make_card("Local")
        remote = self._make_card("Remote")
        result = negotiate(local, remote)
        assert not result.compatible
        assert result.shared_skills == []

    def test_remote_no_auth_required(self) -> None:
        local = self._make_card("Local", skills=[("s1", "S1")])
        remote = self._make_card("Remote", skills=[("s1", "S1")])
        result = negotiate(local, remote)
        assert result.auth_compatible
