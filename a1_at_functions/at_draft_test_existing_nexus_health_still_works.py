# Extracted from C:/!ass-ade/tests/test_new_commands.py:417
# Component id: at.source.ass_ade.test_existing_nexus_health_still_works
from __future__ import annotations

__version__ = "0.1.0"

def test_existing_nexus_health_still_works(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.get_health.return_value = HealthStatus(status="ok")
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app, ["nexus", "health", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"]
        )
    assert result.exit_code == 0
    assert "ok" in result.stdout
