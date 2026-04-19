# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a0_qk_constants/qk_draft_proofbridge.py:41
# Component id: qk.source.ass_ade.run
__version__ = "0.1.0"

    def run(self, ctx: dict) -> dict:
        spec = self.translate(ctx.get("description", ""))
        return {"name": spec.name, "source": spec.source, "has_sorry": spec.has_sorry}
