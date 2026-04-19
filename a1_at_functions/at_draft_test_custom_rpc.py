# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/tests/test_x402_flow.py:264
# Component id: at.source.ass_ade.test_custom_rpc
__version__ = "0.1.0"

    def test_custom_rpc(self) -> None:
        with patch.dict("os.environ", {"BASE_RPC_URL": "https://custom.rpc"}, clear=False):
            config = get_chain_config()
        assert config["rpc_url"] == "https://custom.rpc"
