# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:405
# Component id: at.source.ass_ade.test_wallet_testnet_on
__version__ = "0.1.0"

    def test_wallet_testnet_on(self, tmp_path: Path) -> None:
        result = runner.invoke(
            app, ["wallet", "--config", str(_hybrid_config(tmp_path))],
            env={"ATOMADIC_X402_TESTNET": "1"},
        )
        assert result.exit_code == 0
