# Extracted from C:/!ass-ade/tests/test_search_x402.py:44
# Component id: qk.source.ass_ade.test_search_requires_session_token
from __future__ import annotations

__version__ = "0.1.0"

def test_search_requires_session_token(self, tmp_path: Path) -> None:
    """Search should fail if ATOMADIC_SESSION_TOKEN is not set."""
    result = runner.invoke(
        app,
        ["search", "test query", "--config", str(_hybrid_config(tmp_path))],
        env={"ATOMADIC_SESSION_TOKEN": ""},
    )
    assert result.exit_code == 1
    assert "ATOMADIC_SESSION_TOKEN" in result.stdout
