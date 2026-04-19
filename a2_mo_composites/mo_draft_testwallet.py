# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_testwallet.py:5
# Component id: mo.source.ass_ade.testwallet
__version__ = "0.1.0"

class TestWallet:
    """Test `wallet` command — check x402 wallet status."""

    def test_wallet_status_no_key(self, tmp_path: Path, hybrid_config: Path) -> None:
        """Wallet status should display chain config and warn if key not set."""
        result = runner.invoke(
            app,
            ["wallet", "--config", str(hybrid_config)],
        )
        
        assert result.exit_code == 0
        assert "Wallet" in result.stdout or "wallet" in result.stdout.lower()
