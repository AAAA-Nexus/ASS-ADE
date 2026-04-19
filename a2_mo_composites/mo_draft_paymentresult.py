# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/x402.py:113
# Component id: mo.source.ass_ade.paymentresult
__version__ = "0.1.0"

class PaymentResult:
    """Result of an x402 payment attempt."""
    success: bool
    txid: str = ""
    signature_header: str = ""
    error: str = ""
    testnet: bool = False
