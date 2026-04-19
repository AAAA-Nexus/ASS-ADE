# Extracted from C:/!ass-ade/tests/test_a2a_cli.py:41
# Component id: at.source.ass_ade.testa2avalidatecli
from __future__ import annotations

__version__ = "0.1.0"

class TestA2AValidateCLI:
    def test_validate_valid_card(self, tmp_path: Path) -> None:
        card_file = tmp_path / "agent.json"
        card_file.write_text(json.dumps({
            "name": "TestAgent",
            "description": "A test agent",
            "url": "https://test.com",
            "version": "1.0.0",
            "skills": [{"id": "skill1", "name": "Test Skill"}],
        }), encoding="utf-8")

        result = runner.invoke(app, ["a2a", "validate", str(card_file)])
        assert result.exit_code == 0
        assert "Valid" in result.stdout or "TestAgent" in result.stdout

    def test_validate_missing_fields(self, tmp_path: Path) -> None:
        card_file = tmp_path / "bad.json"
        card_file.write_text(json.dumps({"description": "Missing name"}), encoding="utf-8")

        result = runner.invoke(app, ["a2a", "validate", str(card_file)])
        assert result.exit_code == 1

    def test_validate_missing_file(self) -> None:
        result = runner.invoke(app, ["a2a", "validate", "/nonexistent/agent.json"])
        assert result.exit_code == 1
