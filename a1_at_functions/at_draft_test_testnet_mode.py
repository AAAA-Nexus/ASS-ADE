# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:257
# Component id: at.source.ass_ade.test_testnet_mode
__version__ = "0.1.0"

    def test_testnet_mode(self) -> None:
        with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": "1"}, clear=False):
            config = get_chain_config()
        assert config["chain_id"] == BASE_SEPOLIA_CHAIN_ID
        assert config["testnet"] is True
        assert "sepolia" in config["network_name"].lower()
