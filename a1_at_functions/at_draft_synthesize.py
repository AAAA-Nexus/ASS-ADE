# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_severa.py:20
# Component id: at.source.ass_ade.synthesize
__version__ = "0.1.0"

    def synthesize(self, arch: Arch) -> Agent:
        code = (
            f"class Agent_{arch.name}:\n"
            f"    traits = {arch.traits!r}\n"
            f"    def run(self, ctx):\n"
            f"        return {{'arch': {arch.name!r}}}\n"
        )
        return Agent(name=f"agent_{arch.name}", arch=arch, code=code)
