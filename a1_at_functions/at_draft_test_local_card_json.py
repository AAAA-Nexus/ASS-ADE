# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testa2alocalcardcli.py:11
# Component id: at.source.ass_ade.test_local_card_json
__version__ = "0.1.0"

    def test_local_card_json(self) -> None:
        result = runner.invoke(app, ["a2a", "local-card", "--json"])
        assert result.exit_code == 0
        data = json.loads(result.stdout, strict=False)
        assert data["name"] == "ASS-ADE"
        assert "skills" in data
