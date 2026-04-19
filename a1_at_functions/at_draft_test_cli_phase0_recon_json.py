# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_cli_phase0_recon_json.py:7
# Component id: at.source.a1_at_functions.test_cli_phase0_recon_json
from __future__ import annotations

__version__ = "0.1.0"

def test_cli_phase0_recon_json(tmp_path: Path) -> None:
    _seed_repo(tmp_path)
    result = runner.invoke(
        app,
        [
            "workflow",
            "phase0-recon",
            "Add an MCP tool schema",
            "--path",
            str(tmp_path),
            "--json",
        ],
    )

    assert result.exit_code == 0
    assert '"verdict": "RECON_REQUIRED"' in result.stdout
