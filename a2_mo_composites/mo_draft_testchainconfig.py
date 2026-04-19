# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:249
# Component id: mo.source.ass_ade.testchainconfig
__version__ = "0.1.0"

class TestChainConfig:
    def test_mainnet_by_default(self) -> None:
        with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": ""}, clear=False):
            config = get_chain_config()
        assert config["chain_id"] == BASE_MAINNET_CHAIN_ID
        assert config["testnet"] is False
        assert "mainnet" in config["network_name"].lower()

    def test_testnet_mode(self) -> None:
        with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": "1"}, clear=False):
            config = get_chain_config()
        assert config["chain_id"] == BASE_SEPOLIA_CHAIN_ID
        assert config["testnet"] is True
        assert "sepolia" in config["network_name"].lower()

    def test_custom_rpc(self) -> None:
        with patch.dict("os.environ", {"BASE_RPC_URL": "https://custom.rpc"}, clear=False):
            config = get_chain_config()
        assert config["rpc_url"] == "https://custom.rpc"
