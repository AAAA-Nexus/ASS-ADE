# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:281
# Component id: mo.source.ass_ade.testcompliancecheck
from __future__ import annotations

__version__ = "0.1.0"

class TestComplianceCheck:
    """Test `compliance check` command — run multi-framework compliance audit."""

    def test_compliance_check_success(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Compliance check should evaluate system against multiple frameworks."""
        mock_nx = MagicMock()
        mock_nx.compliance_check.return_value = ComplianceResult(
            system_name="MyAI",
            frameworks=["EU AI Act", "ISO 42001", "NIST RMF"],
            results=[
                {"framework": "EU AI Act", "status": "compliant", "score": 0.92},
                {"framework": "ISO 42001", "status": "partial", "score": 0.78},
            ],
            overall_verdict="COMPLIANT_WITH_MITIGATIONS",
        )

        payload_file = tmp_path / "system.json"
        payload_file.write_text(json.dumps({"name": "MyAI"}), encoding="utf-8")

        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["compliance", "check", str(payload_file), "--config", str(hybrid_config)],
            )

        assert result.exit_code == 0
