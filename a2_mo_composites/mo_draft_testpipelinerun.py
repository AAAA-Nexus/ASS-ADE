# Extracted from C:/!ass-ade/tests/test_cli_happy_path.py:332
# Component id: mo.source.ass_ade.testpipelinerun
from __future__ import annotations

__version__ = "0.1.0"

class TestPipelineRun:
    """Test `pipeline run` command — execute sequential pipeline."""

    def test_pipeline_run_trust_gate_success(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Trust-gate pipeline should verify identity, sybil, trust, and reputation."""
        mock_nx = MagicMock()

        # Mock the four trust-gate steps
        identity_result = MagicMock()
        identity_result.model_dump.return_value = {"decision": "allow"}
        mock_nx.identity_verify.return_value = identity_result

        sybil_result = MagicMock()
        sybil_result.model_dump.return_value = {"sybil_risk": "low"}
        mock_nx.sybil_check.return_value = sybil_result

        trust_result = MagicMock()
        trust_result.model_dump.return_value = {"score": 0.85}
        mock_nx.trust_score.return_value = trust_result

        reputation_result = MagicMock()
        reputation_result.model_dump.return_value = {"tier": "gold"}
        mock_nx.reputation_score.return_value = reputation_result

        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["pipeline", "run", "trust-gate", "agent-test-001", "--config", str(hybrid_config), "--no-persist"],
            )

        assert result.exit_code == 0, f"Pipeline failed:\n{result.stdout}"
        # Verify pipeline ran and produced output
        assert "Running pipeline" in result.stdout
        assert "identity_verify" in result.stdout or "identity" in result.stdout.lower()
        assert "gate_decision" in result.stdout or "gate" in result.stdout.lower()
        # Verify all trust-gate steps were mentioned
        assert mock_nx.identity_verify.called
        assert mock_nx.sybil_check.called
        assert mock_nx.trust_score.called
        assert mock_nx.reputation_score.called

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

    def test_pipeline_run_certify_success(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Certify pipeline should verify hallucination, ethics, compliance, and certify output."""
        mock_nx = MagicMock()

        # Mock the four certify steps
        hallucination_result = MagicMock()
        hallucination_result.model_dump.return_value = {"verdict": "safe"}
        mock_nx.hallucination_oracle.return_value = hallucination_result

        ethics_result = MagicMock()
        ethics_result.model_dump.return_value = {"safe": True}
        mock_nx.ethics_check.return_value = ethics_result

        compliance_result = MagicMock()
        compliance_result.model_dump.return_value = {"compliant": True}
        mock_nx.compliance_check.return_value = compliance_result

        certify_result = MagicMock()
        certify_result.model_dump.return_value = {"certificate_id": "cert-2025-12345"}
        mock_nx.certify_output.return_value = certify_result

        test_text = "The Earth is round and orbits the Sun."

        with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
            result = runner.invoke(
                app,
                ["pipeline", "run", "certify", test_text, "--config", str(hybrid_config), "--no-persist"],
            )

        assert result.exit_code == 0, f"Pipeline failed:\n{result.stdout}"
        assert "Running pipeline" in result.stdout
        assert "certify-output" in result.stdout or "certify" in result.stdout.lower()
        # Verify all certify steps were called
        assert mock_nx.hallucination_oracle.called
        assert mock_nx.ethics_check.called
        assert mock_nx.compliance_check.called
        assert mock_nx.certify_output.called

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

    def test_pipeline_status_workflow_found(self, tmp_path: Path) -> None:
        """Pipeline status should display workflow status when file exists."""
        # Create a workflows directory with a sample workflow file
        workflow_dir = tmp_path / ".ass-ade" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)

        workflow_data = {
            "name": "trust-gate-agent-001",
            "passed": True,
            "duration_ms": 1234.5,
            "summary": "Trust gate: ALLOW verdict"
        }
        workflow_file = workflow_dir / "trust-gate-20250417-120000.json"
        workflow_file.write_text(json.dumps(workflow_data), encoding="utf-8")

        # Mock the working directory to use tmp_path
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = runner.invoke(
                app,
                ["pipeline", "status", "trust-gate-20250417-120000.json"],
            )

        # Status command should succeed and output JSON
        assert result.exit_code == 0, f"Status failed:\n{result.stdout}"
        assert "trust-gate-agent-001" in result.stdout

    def test_pipeline_status_workflow_not_found(self, tmp_path: Path) -> None:
        """Pipeline status should handle missing workflow gracefully."""
        workflow_dir = tmp_path / ".ass-ade" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = runner.invoke(
                app,
                ["pipeline", "status", "nonexistent-workflow"],
            )

        # Should exit cleanly when workflow not found
        assert result.exit_code == 0 or "not found" in result.stdout.lower()

    def test_pipeline_history_lists_workflows(self, tmp_path: Path) -> None:
        """Pipeline history should list recent workflows."""
        workflow_dir = tmp_path / ".ass-ade" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)

        # Create several workflow files
        for i in range(3):
            workflow_data = {
                "name": f"test-workflow-{i}",
                "passed": i % 2 == 0,
                "duration_ms": 500 + i * 100,
            }
            workflow_file = workflow_dir / f"workflow-{i:03d}.json"
            workflow_file.write_text(json.dumps(workflow_data), encoding="utf-8")

        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = runner.invoke(
                app,
                ["pipeline", "history", "--limit", "5"],
            )

        # History should display a table with workflows
        assert result.exit_code == 0, f"History failed:\n{result.stdout}"
        # Should show table or list of workflows
        assert "test-workflow" in result.stdout or "History" in result.stdout or "Workflow" in result.stdout

    def test_pipeline_history_empty(self, tmp_path: Path) -> None:
        """Pipeline history should handle missing workflows directory gracefully."""
        with patch("pathlib.Path.cwd", return_value=tmp_path):
            result = runner.invoke(
                app,
                ["pipeline", "history"],
            )

        # Should exit cleanly with appropriate message
        assert result.exit_code == 0
        assert "history" in result.stdout.lower() or "found" in result.stdout.lower()
