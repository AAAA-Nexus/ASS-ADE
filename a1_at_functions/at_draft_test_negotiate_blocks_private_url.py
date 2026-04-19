# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_negotiate_blocks_private_url.py:7
# Component id: at.source.a1_at_functions.test_negotiate_blocks_private_url
from __future__ import annotations

__version__ = "0.1.0"

def test_negotiate_blocks_private_url(self, tmp_path: Path) -> None:
    result = runner.invoke(
        app, ["a2a", "negotiate", "http://192.168.1.1/.well-known/agent.json",
               "--config", str(_hybrid_config(tmp_path))]
    )
    assert result.exit_code == 1
    assert "Blocked" in result.stdout
