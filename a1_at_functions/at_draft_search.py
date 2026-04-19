# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_severa.py:11
# Component id: at.source.ass_ade.search
__version__ = "0.1.0"

    def search(self) -> list[Arch]:
        self._searches += 1
        base = [
            Arch(name="linear", score=0.5, traits=["simple"]),
            Arch(name="tree", score=0.7, traits=["recursive"]),
            Arch(name="graph", score=0.8, traits=["emergent"]),
        ]
        return sorted(base, key=lambda a: a.score, reverse=True)
