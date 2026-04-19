# Extracted from C:/!ass-ade/.claude/worktrees/adoring-boyd-0e3a8f/src/ass_ade/nexus/client.py:534
# Component id: mo.source.ass_ade.escrow_create
__version__ = "0.1.0"

    def escrow_create(self, amount_usdc: float, sender: str, receiver: str, conditions: list[str], **kwargs: Any) -> EscrowCreated:
        """/v1/escrow/create — lock USDC with release conditions. $0.040/call"""
        return self._post_model("/v1/escrow/create", EscrowCreated, {
            "amount_usdc": amount_usdc, "sender": sender, "receiver": receiver,
            "conditions": conditions, **kwargs,
        })
