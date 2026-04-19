# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_existing_nexus_health_still_works.py:7
# Component id: at.source.a1_at_functions.test_existing_nexus_health_still_works
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
