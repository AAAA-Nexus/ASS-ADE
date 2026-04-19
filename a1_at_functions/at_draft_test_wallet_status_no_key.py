# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_cli_happy_path.py:623
# Component id: at.source.ass_ade.test_wallet_status_no_key
__version__ = "0.1.0"

    def test_wallet_status_no_key(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Wallet status should display chain config and warn if key not set."""
        result = runner.invoke(
            app,
            ["wallet", "--config", str(hybrid_config)],
        )
        
        assert result.exit_code == 0
        assert "Wallet" in result.stdout or "wallet" in result.stdout.lower()
