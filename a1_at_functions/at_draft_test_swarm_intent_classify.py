# Extracted from C:/!ass-ade/tests/test_new_commands.py:705
# Component id: at.source.ass_ade.test_swarm_intent_classify
from __future__ import annotations

__version__ = "0.1.0"

def test_swarm_intent_classify(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.agent_intent_classify.return_value = IntentClassification(primary_intent="search", top_intents=[])
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(app, ["swarm", "intent-classify", "find something",
                                     "--config", str(_hybrid_config(tmp_path)), "--allow-remote"])
    assert result.exit_code == 0
    assert "search" in result.stdout
