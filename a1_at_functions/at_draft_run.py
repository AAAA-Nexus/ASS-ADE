# Extracted from C:/!ass-ade/src/ass_ade/agent/trust_gate.py:52
# Component id: at.source.ass_ade.run
from __future__ import annotations

__version__ = "0.1.0"

def run(self, ctx: dict) -> dict:
    ok = self.pre_action_verify(ctx.get("action", {}))
    return {"allowed": ok}
