# Extracted from C:/!ass-ade-evoMERGE-g3-20260419-003649/a1_at_functions/at_draft_synthesize.py:7
# Component id: at.source.a1_at_functions.synthesize
from __future__ import annotations

__version__ = "0.1.0"

def synthesize(self, arch: Arch) -> Agent:
    code = (
        f"class Agent_{arch.name}:\n"
        f"    traits = {arch.traits!r}\n"
        f"    def run(self, ctx):\n"
        f"        return {{'arch': {arch.name!r}}}\n"
    )
    return Agent(name=f"agent_{arch.name}", arch=arch, code=code)
