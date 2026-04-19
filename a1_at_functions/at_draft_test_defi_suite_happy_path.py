# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_test_defi_suite_happy_path.py:7
# Component id: at.source.a1_at_functions.test_defi_suite_happy_path
from __future__ import annotations

__version__ = "0.1.0"

def test_defi_suite_happy_path(method_name, response_json):
    """Test DeFi suite methods (happy path)."""
    def handler(request):
        return httpx.Response(200, json=response_json)

    transport = httpx.MockTransport(handler)
    with NexusClient(base_url="https://atomadic.tech", transport=transport) as client:
        if method_name == "defi_optimize":
            result = client.defi_optimize(protocol="uniswap", position_size_usdc=1000.0)
        elif method_name == "defi_risk_score":
            result = client.defi_risk_score(protocol="uniswap", position={})
        elif method_name == "defi_oracle_verify":
            result = client.defi_oracle_verify(pool="uniswap_pool", tvl_usdc=1000000.0)
        elif method_name == "defi_liquidation_check":
            result = client.defi_liquidation_check(position={})
        elif method_name == "defi_bridge_verify":
            result = client.defi_bridge_verify(bridge="bridge_name", amount_usdc=1000.0)
        elif method_name == "defi_contract_audit":
            result = client.defi_contract_audit(contract_address="0x123", source_code="solidity code")
        else:  # defi_yield_optimize
            result = client.defi_yield_optimize(capital_usdc=10000.0, protocols=["uniswap"])
        assert result is not None
