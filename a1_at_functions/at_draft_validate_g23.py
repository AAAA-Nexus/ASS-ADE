# Extracted from C:/!ass-ade/.claude/worktrees/beautiful-dubinsky-c2cb48/a2_mo_composites/mo_draft_sam.py:30
# Component id: at.source.ass_ade.validate_g23
__version__ = "0.1.0"

    def validate_g23(self, intent: str, impl: str) -> bool:
        vi = vector_embed(intent)
        vc = vector_embed(impl)
        sim = _cosine(vi, vc)
        distance = max(0.0, 1.0 - sim) * 10.0
        return distance <= self._g23_threshold
