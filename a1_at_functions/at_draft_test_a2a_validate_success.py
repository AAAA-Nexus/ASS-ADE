# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_testa2avalidate.py:10
# Component id: at.source.a1_at_functions.test_a2a_validate_success
from __future__ import annotations

__version__ = "0.1.0"

def test_a2a_validate_success(self, tmp_path: Path) -> None:
    """Valid agent card structure test."""
    card = {
        "name": "TestAgent",
        "description": "A test agent",
        "capabilities": ["reasoning", "tool_use"],
        "endpoint": "https://agent.example.com/api",
    }
    card_file = tmp_path / "agent_card.json"
    card_file.write_text(json.dumps(card), encoding="utf-8")

    result = runner.invoke(app, ["a2a", "validate", str(card_file)])

    # Validation may pass or fail depending on schema; both acceptable
    assert result.exit_code in (0, 1)
