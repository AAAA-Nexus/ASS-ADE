# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a0_qk_constants/qk_draft_proofbridge.py:43
# Component id: qk.source.a0_qk_constants.run
from __future__ import annotations

__version__ = "0.1.0"

def run(self, ctx: dict) -> dict:
    spec = self.translate(ctx.get("description", ""))
    return {"name": spec.name, "source": spec.source, "has_sorry": spec.has_sorry}
