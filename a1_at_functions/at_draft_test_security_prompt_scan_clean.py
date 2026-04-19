# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_security_prompt_scan_clean.py:7
# Component id: at.source.a1_at_functions.test_security_prompt_scan_clean
from __future__ import annotations

__version__ = "0.1.0"

def test_security_prompt_scan_clean(tmp_path: Path) -> None:
    mock_nx = MagicMock()
    mock_nx.prompt_inject_scan.return_value = PromptScanResult(threat_detected=False, threat_level="none", confidence=0.99)
    with patch("ass_ade.cli.NexusClient", return_value=_make_ctx_mgr(mock_nx)):
        result = runner.invoke(
            app,
            ["security", "prompt-scan", "Tell me about Python.", "--config", str(_hybrid_config(tmp_path)), "--allow-remote"],
        )
    assert result.exit_code == 0
    assert "CLEAN" in result.stdout
