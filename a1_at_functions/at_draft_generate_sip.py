# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_generate_sip.py:7
# Component id: at.source.a1_at_functions.generate_sip
from __future__ import annotations

__version__ = "0.1.0"

def generate_sip(self, top: list[Candidate]) -> SIP:
    head = top[:3]
    summary = "; ".join(f"{c.id}@{c.fitness:.2f}" for c in head)
    return SIP(top=head, summary=summary)
