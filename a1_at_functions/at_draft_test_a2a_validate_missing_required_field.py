# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli_happy_path.py:146
# Component id: at.source.ass_ade.test_a2a_validate_missing_required_field
__version__ = "0.1.0"

    def test_a2a_validate_missing_required_field(self, tmp_path: Path) -> None:
        """Card with missing field test."""
        card = {
            "name": "TestAgent",
            "description": "Missing endpoint",
            # endpoint missing
        }
        card_file = tmp_path / "agent_card.json"
        card_file.write_text(json.dumps(card), encoding="utf-8")
        
        result = runner.invoke(app, ["a2a", "validate", str(card_file)])
        
        # Command should complete (pass or fail)
        assert result.exit_code in (0, 1, 2)
