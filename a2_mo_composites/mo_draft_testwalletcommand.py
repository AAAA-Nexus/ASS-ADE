# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:396
# Component id: mo.source.ass_ade.testwalletcommand
__version__ = "0.1.0"

class TestWalletCommand:
    def test_wallet_shows_status(self, tmp_path: Path) -> None:
        result = runner.invoke(
            app, ["wallet", "--config", str(_hybrid_config(tmp_path))],
            env={"ATOMADIC_X402_TESTNET": "1", "ATOMADIC_WALLET_KEY": ""},
        )
        assert result.exit_code == 0
        assert "Testnet Mode" in result.stdout or "x402" in result.stdout

    def test_wallet_testnet_on(self, tmp_path: Path) -> None:
        result = runner.invoke(
            app, ["wallet", "--config", str(_hybrid_config(tmp_path))],
            env={"ATOMADIC_X402_TESTNET": "1"},
        )
        assert result.exit_code == 0
