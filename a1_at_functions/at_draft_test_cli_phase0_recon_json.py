# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_recon_context.py:159
# Component id: at.source.ass_ade.test_cli_phase0_recon_json
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
