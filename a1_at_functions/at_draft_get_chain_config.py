# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/x402.py:183
# Component id: at.source.ass_ade.get_chain_config
__version__ = "0.1.0"

def get_chain_config() -> dict[str, Any]:
    """Get chain configuration based on testnet/mainnet mode."""
    testnet = is_testnet()
    return {
        "testnet": testnet,
        "chain_id": BASE_SEPOLIA_CHAIN_ID if testnet else BASE_MAINNET_CHAIN_ID,
        "rpc_url": os.environ.get(
            "BASE_RPC_URL",
            BASE_SEPOLIA_RPC if testnet else BASE_MAINNET_RPC,
        ),
        "usdc_address": USDC_BASE_SEPOLIA if testnet else USDC_BASE_MAINNET,
        "treasury": ATOMADIC_TREASURY,
        "network_name": "Base Sepolia (testnet)" if testnet else "Base (mainnet)",
    }
