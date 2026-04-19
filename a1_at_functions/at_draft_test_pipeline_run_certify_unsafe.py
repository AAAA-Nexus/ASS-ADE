# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:442
# Component id: at.source.ass_ade.test_pipeline_run_certify_unsafe
from __future__ import annotations

__version__ = "0.1.0"

def test_pipeline_run_certify_unsafe(self, tmp_path: Path, hybrid_config: Path) -> None:
    """Certify pipeline should handle unsafe content."""
    mock_nx = MagicMock()

    hallucination_result = MagicMock()
    hallucination_result.model_dump.return_value = {"verdict": "unsafe"}
    mock_nx.hallucination_oracle.return_value = hallucination_result

    ethics_result = MagicMock()
    ethics_result.model_dump.return_value = {"safe": False}
    mock_nx.ethics_check.return_value = ethics_result

    compliance_result = MagicMock()
    compliance_result.model_dump.return_value = {"compliant": False}
    mock_nx.compliance_check.return_value = compliance_result

    certify_result = MagicMock()
    certify_result.model_dump.return_value = {"certificate_id": None}
    mock_nx.certify_output.return_value = certify_result

    test_text = "Some potentially harmful content here."

    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["pipeline", "run", "certify", test_text, "--config", str(hybrid_config), "--no-persist"],
        )

    # Pipeline runs to completion even with unsafe verdict (fail_fast=False)
    assert result.exit_code in (0, 1), f"Pipeline error:\n{result.stdout}"
    assert "Running pipeline" in result.stdout
