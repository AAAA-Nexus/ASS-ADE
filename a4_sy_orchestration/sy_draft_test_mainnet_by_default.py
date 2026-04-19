# Extracted from C:/!ass-ade/tests/test_x402_flow.py:250
# Component id: sy.source.ass_ade.test_mainnet_by_default
from __future__ import annotations

__version__ = "0.1.0"

def test_mainnet_by_default(self) -> None:
    with patch.dict("os.environ", {"ATOMADIC_X402_TESTNET": ""}, clear=False):
        config = get_chain_config()
    assert config["chain_id"] == BASE_MAINNET_CHAIN_ID
    assert config["testnet"] is False
    assert "mainnet" in config["network_name"].lower()
