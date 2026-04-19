# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/x402.py:178
# Component id: at.source.ass_ade.is_testnet
__version__ = "0.1.0"

def is_testnet() -> bool:
    """Check if testnet mode is enabled."""
    return os.environ.get("ATOMADIC_X402_TESTNET", "").strip() in ("1", "true", "yes")
