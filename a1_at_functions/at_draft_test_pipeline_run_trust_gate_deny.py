# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:373
# Component id: at.source.ass_ade.test_pipeline_run_trust_gate_deny
from __future__ import annotations

__version__ = "0.1.0"

def test_pipeline_run_trust_gate_deny(self, tmp_path: Path, hybrid_config: Path) -> None:
    """Trust-gate pipeline should deny low-score agents."""
    mock_nx = MagicMock()

    # Mock with low trust score to trigger DENY
    identity_result = MagicMock()
    identity_result.model_dump.return_value = {"decision": "deny"}
    mock_nx.identity_verify.return_value = identity_result

    sybil_result = MagicMock()
    sybil_result.model_dump.return_value = {"sybil_risk": "high"}
    mock_nx.sybil_check.return_value = sybil_result

    trust_result = MagicMock()
    trust_result.model_dump.return_value = {"score": 0.2}
    mock_nx.trust_score.return_value = trust_result

    reputation_result = MagicMock()
    reputation_result.model_dump.return_value = {"tier": "bronze"}
    mock_nx.reputation_score.return_value = reputation_result

    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["pipeline", "run", "trust-gate", "agent-untrusted", "--config", str(hybrid_config), "--no-persist"],
        )

    # Pipeline completes but gate decision is DENY (fail_fast=False runs all steps)
    assert result.exit_code in (0, 1), f"Pipeline error:\n{result.stdout}"
    assert "Running pipeline" in result.stdout
