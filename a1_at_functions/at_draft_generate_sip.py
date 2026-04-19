# Extracted from C:/!ass-ade/src/ass_ade/agent/ide.py:51
# Component id: at.source.ass_ade.generate_sip
from __future__ import annotations

__version__ = "0.1.0"

def generate_sip(self, top: list[Candidate]) -> SIP:
    head = top[:3]
    summary = "; ".join(f"{c.id}@{c.fitness:.2f}" for c in head)
    return SIP(top=head, summary=summary)
