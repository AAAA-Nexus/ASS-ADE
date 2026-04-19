# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_oracle_hallucination_writes_json_out.py:7
# Component id: at.source.a1_at_functions.test_oracle_hallucination_writes_json_out
from __future__ import annotations

__version__ = "0.1.0"

def test_oracle_hallucination_writes_json_out(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.hallucination_oracle.return_value = HallucinationResult(policy_epsilon=0.05, verdict="caution")
    out_file = tmp_path / "result.json"
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["oracle", "hallucination", "test", "--config", str(_hybrid_config(tmp_path)), "--allow-remote", "--json-out", str(out_file)],
        )
    assert result.exit_code == 0
    data = json.loads(out_file.read_text())
    assert data["verdict"] == "caution"
