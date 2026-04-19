# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_atomadic.py:249
# Component id: at.source.a1_at_functions.describe_self
from __future__ import annotations

__version__ = "0.1.0"

def describe_self(self) -> str:
    try:
        return render_atomadic_help(self.working_dir)
    except Exception:
        return (
            "I'm Atomadic, the front door of ASS-ADE.\n\n"
            "I can rebuild, design, document, lint, certify, enhance, scan, "
            "and evolve codebases. Just tell me what you want in plain English."
        )
