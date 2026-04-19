# Extracted from C:/!ass-ade/tests/test_new_commands.py:715
# Component id: at.source.ass_ade.test_swarm_contradiction
from __future__ import annotations

__version__ = "0.1.0"

def test_swarm_contradiction(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.agent_contradiction.return_value = ContradictionResult(contradicts=True, confidence=0.95)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["swarm", "contradiction", "A is true", "A is false",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "CONTRADICTS" in result.stdout
