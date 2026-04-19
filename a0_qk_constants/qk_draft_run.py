# Extracted from C:/!ass-ade/src/ass_ade/agent/proofbridge.py:56
# Component id: qk.source.ass_ade.run
from __future__ import annotations

__version__ = "0.1.0"

def run(self, ctx: dict) -> dict:
    spec = self.translate(ctx.get("description", ""))
    return {"name": spec.name, "source": spec.source, "has_sorry": spec.has_sorry}
