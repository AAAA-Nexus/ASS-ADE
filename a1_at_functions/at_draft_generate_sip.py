# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_ide.py:34
# Component id: at.source.ass_ade.generate_sip
__version__ = "0.1.0"

    def generate_sip(self, top: list[Candidate]) -> SIP:
        head = top[:3]
        summary = "; ".join(f"{c.id}@{c.fitness:.2f}" for c in head)
        return SIP(top=head, summary=summary)
